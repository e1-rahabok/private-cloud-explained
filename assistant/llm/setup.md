# LLM VM setup runbook

Builds the CPU-only VM that serves the chat model for Ask. Design and reasons are in [08 Assistant and local LLM](../../docs/08-assistant-and-llm.md). This file is the steps.

Written so that a person or Claude Code can follow it top to bottom. Each step ends with a check. Do not move on until the check passes.

## Decisions this runbook assumes

| Item | Value | Status |
| --- | --- | --- |
| Guest OS | Ubuntu Server 24.04 LTS | Decided (D-029) |
| VMware Tools | `open-vm-tools` from Ubuntu packages | Decided (D-029) |
| Engine | llama.cpp `llama-server`, built from a pinned release tag | Proposed (D-005) |
| Chat model | Gemma 4 26B-A4B instruct, GGUF, Q4_K_M | Proposed (D-002) |
| Internet on the VM | During setup only. Removed in step 11 (N1) | Given |
| Embedding model | Not covered here until D-004 is decided | Open |

## Inputs

Fill these in your private copy. Do not commit real addresses, user names or secrets to the public template.

| Input | Example | Notes |
| --- | --- | --- |
| `VM_NAME` | `llm-01` | vSphere VM name and hostname |
| `VM_IP` | `<ip>` | Static address or DHCP reservation |
| `SSH_USER` | `<admin user>` | Created by the Ubuntu installer |
| `SITE_IP` | `<ip of the web VM>` | Only client allowed to call the API |
| `LLM_PORT` | `8080` | |

## Running this with Claude Code

- Claude Code runs on your workstation and reaches the VM over SSH: `ssh $SSH_USER@$VM_IP '<command>'`.
- Set up SSH key login first. Claude Code cannot answer password prompts.
- Shell variables (`TAG`, `REPO`, `REV`, `FILE`, `SHA`) do not carry over between separate SSH calls. Set them again, or run a step's commands in one call.
- Give `SSH_USER` passwordless sudo for the duration of setup (`/etc/sudoers.d/90-setup`), and remove it at the end (step 11).
- Step 1 is done in the vSphere Client. Claude Code may do it with PowerCLI or `govc` if you give it vCenter access, but the settings are the same.
- Never print, log or commit the API key or a Hugging Face token. The commands below read them from files on the VM.

## Layout on the VM

| Path | Contents | Owner |
| --- | --- | --- |
| `/opt/llm/src/llama.cpp` | llama.cpp source at the pinned tag | `llm` |
| `/opt/llm/bin` | `llama-server`, `llama-bench`, `llama-cli` | `root` |
| `/opt/llm/models` | GGUF files | `llm` |
| `/etc/llm/llama-server.env` | Server settings | `root` |
| `/etc/llm/api-key` | API key, mode 0640 | `root:llm` |
| `/etc/systemd/system/llama-server.service` | Service unit | `root` |

Templates for the env file and the unit are next to this file: [llama-server.env.example](llama-server.env.example) and [llama-server.service](llama-server.service).

## Step 1. Create the VM in vSphere

Apply the settings from [08, "vSphere configuration"](../../docs/08-assistant-and-llm.md#vsphere-configuration).

| Setting | Value |
| --- | --- |
| Guest OS family and version | Linux, Ubuntu Linux (64-bit) |
| Compatibility | Virtual hardware version 20 or later |
| CPU | 16 vCPU, 16 cores per socket (one socket) |
| CPU reservation or shares | High shares, or a reservation agreed with the virtualisation team |
| Memory | 128 GB, **Reserve all guest memory** ticked |
| Disk | 200 GB, thin is fine |
| SCSI controller | VMware Paravirtual |
| Network | VMXNET3 |
| Host | One with all memory channels populated and the newest CPU generation available |
| EVC | Cluster baseline must not mask AVX-512 (and AMX on Xeon) |
| Boot media | Ubuntu Server 24.04 LTS ISO from ubuntu.com |

Check: the VM summary shows hardware version 20 or later and memory reservation 128 GB.

## Step 2. Install Ubuntu Server 24.04 LTS

- Use the standard server install, not minimized.
- Set hostname to `VM_NAME`, create `SSH_USER`.
- Tick **Install OpenSSH server**.
- Do not select any snaps.

After first boot:

```bash
sudo apt update && sudo apt -y full-upgrade
sudo reboot
```

Check: `lsb_release -d` shows Ubuntu 24.04, and SSH with a key works.

## Step 3. VMware Tools

Ubuntu ships VMware Tools as the `open-vm-tools` package. The server installer usually adds it when it detects VMware, but check. Use the Ubuntu package, not the VMware Tools ISO. VMware recommends `open-vm-tools` for Linux distributions that ship it.

```bash
systemctl is-active open-vm-tools || {
  sudo apt install -y open-vm-tools
  sudo systemctl enable --now open-vm-tools
}
vmware-toolbox-cmd -v
```

Check:

- `systemctl is-active open-vm-tools` prints `active`.
- In the vSphere Client, the VM summary shows VMware Tools **Running**, version **Guest Managed**, and the VM's IP address.

## Step 4. Verify CPU, memory and NUMA inside the guest

```bash
nproc
free -g
lscpu | grep -E 'Model name|Socket|NUMA node'
grep -o -w -E 'avx2|avx512f|avx512_vnni|avx512_bf16|amx_tile|amx_int8|amx_bf16' /proc/cpuinfo | sort -u
```

Check:

| Item | Expected |
| --- | --- |
| `nproc` | 16 |
| `free -g` total | About 125 |
| NUMA nodes | 1 |
| `avx512f` | Present. If missing, check EVC and hardware version before going further |
| `amx_*` | Present on 4th and 5th generation Xeon. Not present on AMD EPYC, which is expected |

Record the CPU model and flags in `assistant/models.md` under "Host".

## Step 5. Packages, user and directories

```bash
sudo apt install -y build-essential cmake git curl jq ca-certificates libcurl4-openssl-dev libssl-dev
sudo useradd --system --home /opt/llm --shell /usr/sbin/nologin llm
sudo mkdir -p /opt/llm/src /opt/llm/bin /opt/llm/models /etc/llm
sudo chown -R llm:llm /opt/llm/src /opt/llm/models
```

Check: `id llm` succeeds and the directories exist.

## Step 6. Build llama.cpp at a pinned tag

Use the newest release tag at install time. Record the tag. Do not track `master`.

```bash
TAG=$(curl -s https://api.github.com/repos/ggml-org/llama.cpp/releases/latest | jq -r .tag_name)
echo "$TAG"
sudo -u llm git clone https://github.com/ggml-org/llama.cpp /opt/llm/src/llama.cpp
cd /opt/llm/src/llama.cpp
sudo -u llm git checkout "$TAG"
sudo -u llm cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON -DBUILD_SHARED_LIBS=OFF
sudo -u llm cmake --build build --config Release -j "$(nproc)"
sudo install -m 0755 build/bin/llama-server build/bin/llama-bench build/bin/llama-cli /opt/llm/bin/
/opt/llm/bin/llama-server --version
```

`GGML_NATIVE=ON` builds for the CPU of this VM, so AVX-512 and AMX are used when the guest sees them. A binary built here may not run on an older host. Rebuild if the VM moves to a different CPU generation.

Flag names in llama.cpp change between releases. Confirm the flags this runbook uses exist in the pinned build:

```bash
/opt/llm/bin/llama-server --help | grep -E -- '--api-key-file|--reasoning-budget|--jinja|--mlock|--parallel|--no-webui|--metrics|--alias'
```

Check: `--version` prints the tag, and every flag above is listed. If a flag is missing or renamed, adjust [llama-server.service](llama-server.service) and note the change in this file.

## Step 7. Download the model and verify its checksum

```bash
REPO=ggml-org/gemma-4-26B-A4B-it-GGUF
REV=$(curl -s "https://huggingface.co/api/models/$REPO" | jq -r .sha)
echo "$REV"
curl -s "https://huggingface.co/api/models/$REPO/tree/$REV" \
  | jq -r '.[] | select(.path|endswith(".gguf")) | [.path, .size, (.lfs.oid // "")] | @tsv'
```

The listing shows each file name, size in bytes and SHA-256. Pick the `Q4_K_M` file. Skip any `mmproj` file: it is the vision projector and Ask is text only. If the quant is split into parts (`-00001-of-0000N`), download every part.

```bash
FILE=<Q4_K_M file name from the listing>
SHA=<sha256 from the listing>
sudo -u llm curl -fL --retry 5 -C - -o "/opt/llm/models/$FILE" \
  "https://huggingface.co/$REPO/resolve/$REV/$FILE"
echo "$SHA  /opt/llm/models/$FILE" | sha256sum -c -
```

If the API or download returns 401 or 403, the repository is gated:

1. Accept the model licence on its Hugging Face page with an account the organisation approves (D-003).
2. Create a read-only token.
3. Add `-H "Authorization: Bearer $HF_TOKEN"` to both `curl` calls, with `HF_TOKEN` set only in the shell session.
4. `unset HF_TOKEN` afterwards. Do not save the token on the VM or in Git.

If `ggml-org` has no Q4_K_M file, use another publisher of the same model (for example `bartowski/google_gemma-4-26B-A4B-it-GGUF`) and record which one.

Check: `sha256sum -c` prints `OK`. File size is about 17 GB.

Record in [assistant/models.md](../models.md): repository, revision `REV`, file name, size, SHA-256, licence, download date.

## Step 8. Configure and start the service

API key, generated on the VM and never printed:

```bash
sudo sh -c 'umask 027; openssl rand -hex 32 > /etc/llm/api-key'
sudo chown root:llm /etc/llm/api-key
```

The web VM's `/api/ask` needs the same key. Copy it from the VM to the site's secret store directly. It does not pass through Git, chat or logs.

Settings and unit, from the templates in this folder:

```bash
sudo install -m 0644 llama-server.env.example /etc/llm/llama-server.env
sudo sed -i "s|^LLM_MODEL=.*|LLM_MODEL=/opt/llm/models/$FILE|" /etc/llm/llama-server.env
sudo install -m 0644 llama-server.service /etc/systemd/system/llama-server.service
sudo systemctl daemon-reload
sudo systemctl enable --now llama-server
```

Copy the two template files to the VM first (`scp`), or create them with the same content.

Firewall. Allow SSH before enabling, or the session is cut off:

```bash
sudo ufw allow OpenSSH
sudo ufw allow from "$SITE_IP" to any port 8080 proto tcp
sudo ufw --force enable
sudo ufw status
```

Check:

```bash
systemctl is-active llama-server
journalctl -u llama-server -n 100 --no-pager | grep -E 'system_info|AVX512|AMX|listening|error'
curl -s http://127.0.0.1:8080/health
```

- Service is `active`.
- The `system_info` log line shows `AVX512 = 1` (and `AMX_INT8 = 1` on Xeon with AMX).
- `/health` returns `{"status":"ok"}`. While the model loads it returns 503. Loading 17 GB takes up to a minute.

## Step 9. Smoke tests

Run on the VM. The key is read from the file and not echoed.

```bash
KEY_HDR="Authorization: Bearer $(sudo cat /etc/llm/api-key)"

# 1. Key is enforced
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/v1/models          # expect 401
curl -s -H "$KEY_HDR" http://127.0.0.1:8080/v1/models | jq -r '.data[].id'        # expect the alias

# 2. Grounded answer, reasoning off
cat > /tmp/ask.json <<'EOF'
{
  "model": "gemma-4-26b-a4b-q4",
  "temperature": 0.2,
  "max_tokens": 300,
  "messages": [
    {"role": "system", "content": "Answer only from the passages. Cite passages as [n]. If the passages do not answer the question, say so."},
    {"role": "user", "content": "Passages:\n[1] To reset the lab vCenter password, run `vc-reset --user admin` on the appliance shell.\n[2] Backups run nightly at 01:00.\n\nQuestion: How do I reset the vCenter password?"}
  ]
}
EOF
curl -s -H "$KEY_HDR" -H 'Content-Type: application/json' \
  -d @/tmp/ask.json http://127.0.0.1:8080/v1/chat/completions \
  | jq '{answer: .choices[0].message.content, reasoning: .choices[0].message.reasoning_content, timings}'

# 3. Unanswerable question
sed -i 's|How do I reset the vCenter password?|What is the lunch menu?|' /tmp/ask.json
curl -s -H "$KEY_HDR" -H 'Content-Type: application/json' \
  -d @/tmp/ask.json http://127.0.0.1:8080/v1/chat/completions \
  | jq -r '.choices[0].message.content'

# 4. Three users at once
for i in 1 2 3; do
  curl -s -H "$KEY_HDR" -H 'Content-Type: application/json' -d @/tmp/ask.json \
    http://127.0.0.1:8080/v1/chat/completions -o /tmp/par$i.json &
done; wait
jq -r '.timings | "\(.prompt_per_second) pp/s  \(.predicted_per_second) tg/s"' /tmp/par*.json
rm -f /tmp/ask.json /tmp/par*.json
```

Check:

| Test | Pass when |
| --- | --- |
| 1 | 401 without key, model alias with key |
| 2 | Answer quotes `vc-reset --user admin` exactly and cites [1]. `reasoning` is null or empty |
| 3 | Model says the passages do not answer the question |
| 4 | All three return an answer. No errors in `journalctl -u llama-server` |

If `reasoning` is not empty in test 2, the reasoning flag did not take effect. Add `--chat-template-kwargs '{"enable_thinking":false}'` to the unit, restart and repeat.

From the web VM, confirm the network path: `curl -s http://$VM_IP:8080/health`. From any other machine the port must not answer.

## Step 10. Baseline benchmark

Stop the service so the benchmark does not compete with it:

```bash
sudo systemctl stop llama-server
sudo -u llm /opt/llm/bin/llama-bench -m "/opt/llm/models/$FILE" -t 16 -p 512,2048 -n 128 -r 3
sudo systemctl start llama-server
```

`pp` is prompt processing, `tg` is generation, both in tokens per second.

Check, against target N5 (first word within 20 s):

- Time to first token for a 3,000-token prompt is roughly 3000 / `pp2048`. It should be well under 20 s.
- `tg128` of about 10 tokens per second or more reads comfortably. Below 5 is slow.

Record the table, llama.cpp tag, model file and host CPU in `assistant/eval/` (for example `assistant/eval/bench-<date>-gemma4-26b-q4.md`). These are the first measured figures for this hardware. Until they exist, no speed claim is made (see [12](../../docs/12-design-considerations.md)).

## Step 11. Finish

- Remove outbound internet access (N1, [09](../../docs/09-security-and-governance.md)). Prefer the network firewall. On the VM as well: `sudo ufw default deny outgoing`, then `sudo ufw allow out` rules only for internal DNS, NTP and the internal package mirror, if one exists. Check: `curl -m 5 -s -o /dev/null https://huggingface.co; echo $?` prints a non-zero code, and `/health` from the web VM still works.
- Remove passwordless sudo: `sudo rm /etc/sudoers.d/90-setup`.
- Reboot once and confirm `llama-server` comes back on its own and `/health` is ok.
- Take a VM snapshot only as a short-lived rollback point. Delete it within a few days; snapshots slow I/O and memory-reserved VMs.

## Upgrades and rollback

- Change one thing at a time: llama.cpp tag, model file, quantisation or settings.
- Downloads need outbound access, which is off in service. Open it for the change window only, or bring files in through an approved transfer and verify the SHA-256.
- Before replacing the binary, keep the old one: `sudo cp -a /opt/llm/bin /opt/llm/bin.prev`. Keep the previous model file until the new one passes.
- After any change, re-run steps 9 and 10 and the evaluation set (see [08, "Quality control"](../../docs/08-assistant-and-llm.md#quality-control)).
- Update `assistant/models.md`.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `/health` stays 503 | Model still loading, or failed to load | `journalctl -u llama-server -n 200` |
| Service fails with an mlock error | Memory lock limit | Unit has `LimitMEMLOCK=infinity`. Check it was installed and `daemon-reload` ran |
| `AVX512 = 0` in `system_info` | EVC baseline, old hardware version, or binary built elsewhere | Fix the VM in step 1, then rebuild in step 6 |
| Generation much slower than expected | Host memory channels not populated, NUMA spill, CPU contention | Check host config with the virtualisation team. Confirm 1 NUMA node and reservations |
| Long wait before the first word | Prompt too large | Reduce retrieved context. See [08, "Why retrieval"](../../docs/08-assistant-and-llm.md#why-retrieval-and-not-the-whole-guide) |
| Unknown option at start | Flag renamed in this llama.cpp tag | `llama-server --help`, fix the unit |

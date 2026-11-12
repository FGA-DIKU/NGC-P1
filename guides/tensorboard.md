# TensorBoard on worker01

How to view TensorBoard logs from the cluster in a browser on the Omnissa desktop.

| Name       | What it is                                      |
|------------|-------------------------------------------------|
| `omnissa`  | The virtual desktop (Omnissa Horizon)           |
| `login`    | Login node (keep load off this one)             |
| `worker01` | Interactive node, where TensorBoard runs        |

TensorBoard runs on worker01 and only listens on worker01's localhost. An SSH
tunnel from omnissa (through login) forwards a local port to it.

```
omnissa browser --> localhost:6006 --ssh--> login --ssh--> worker01:127.0.0.1:6006 (TensorBoard)
```

---

## Prerequisites (one-time)

- A venv with TensorBoard on worker01
- Training must write **TensorBoard event files** (`events.out.tfevents.*`).
  In Lightning, add a TensorBoardLogger:

  ```python
  from lightning.pytorch.loggers import TensorBoardLogger

  trainer = Trainer(
      ...,
      logger=[
          ...,
          TensorBoardLogger(save_dir=SAVE_DIR, name="tb"),
      ],
  )
  ```

---

## Step 1: Start TensorBoard on worker01

```bash
# on worker01
tmux new -s tb
source ~/<YOUR_ENV>/bin/activate
tensorboard --logdir /path/to/SAVE_DIR/ --reload_interval 60
```

Wait for `TensorBoard ... at http://127.0.0.1:6006/`, then detach with **Ctrl-b, d**.
It keeps running after you log out.

- `--logdir`: point it at **your own** experiment folder, not a big shared directory.
- The port `6006` can differ depending on usage. Check your `TensorBoard ...` call for the correct one

## Step 2: Open the tunnel from omnissa

Open a **new terminal on omnissa** (check the prompt is not login/worker01):

```bash
ssh -J login -N -L 6006:127.0.0.1:6006 worker01
```

After the password(s), it looks like it hangs. That means it works. Leave it open.

If `-J` doesn't work, use two hops instead:

```bash
# on omnissa
ssh -L 6006:127.0.0.1:16006 login
# then, inside that session on login
ssh -N -L 16006:127.0.0.1:6006 worker01
```

## Step 3: Open the browser on omnissa

Go to **http://localhost:6006**.

---

## Stopping

- Tunnel: **Ctrl-c** in the tunnel terminal on omnissa.
- TensorBoard: on worker01, `tmux attach -t tb`, then **Ctrl-c**.
  Please stop it when you're done, rather than leaving it running for weeks.

Next time, if TensorBoard is still running, only repeat Step 2 and Step 3.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `code 400, message Bad request version (...)` in TensorBoard's output | Browser is using HTTPS. Type `http://localhost:6006` explicitly, or try `http://127.0.0.1:6006`, or turn off "HTTPS-only" / "Always use secure connections" |
| `Could not resolve hostname` | Wrong hostname, or you ran the command on login instead of omnissa |
| "No dashboards are active" | No event files under `--logdir`. Check with `find /path -name "events.out.tfevents*"` |
| `TensorFlow installation not found` | Harmless. TensorBoard works without TensorFlow |

---

## Resource use

- **worker01**: one TensorBoard process. Memory grows with the number of runs/metrics
  under `--logdir`. CPU is near idle. It rescans the log folder every `--reload_interval`.
- **login**: only relays the encrypted SSH traffic. Negligible.
- **omnissa**: SSH client + browser.

Keep it light: narrow `--logdir`, `--reload_interval 60`, stop it when done.
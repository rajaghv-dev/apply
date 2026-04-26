# LP-013 | Video Analytics: CV Pipelines + Edge Deployment

**Domain**: Computer Vision × Embedded × AI  
**Priority**: P2 — strong cross-domain bridge for surveillance/industrial IoT/autonomous systems  
**Effort**: 5–7 days  
**STATUS**: TODO

---

## Why this matters

Video analytics (CCTV, industrial inspection, traffic analysis, safety monitoring)
is one of the largest deployed AI verticals. It combines:
- Computer vision (object detection, tracking, segmentation)
- Edge computing (deploy on embedded hardware, not cloud)
- Systems engineering (latency, throughput, reliability)
- Domain knowledge (surveillance, safety, manufacturing)

Your embedded + hardware background makes you unusually qualified for this.
Most CV engineers don't understand the hardware constraints. Most hardware engineers
don't know CV. You can bridge both.

Gaps closed: `computer_vision`, `edge_ai`, connects `embedded_firmware` + `ml_frameworks`

---

## Learning objectives

- [ ] Understand the CV pipeline: capture → preprocess → infer → postprocess → output
- [ ] Know the key object detection models: YOLO, SSD, Faster R-CNN — when to use each
- [ ] Deploy a model on edge hardware (Raspberry Pi, Jetson Nano, or simulated)
- [ ] Implement object tracking (ByteTrack, SORT, DeepSORT)
- [ ] Understand the latency/accuracy tradeoff for real-time video
- [ ] Build a complete CCTV analytics pipeline: motion detection → object detection → alert

---

## Resources

### Day 1 — Computer Vision foundations
- [ ] Fast.ai Practical Deep Learning → Lesson 1 (free, practical focus)
- [ ] Read: "You Only Look Once: Unified, Real-Time Object Detection" (YOLO paper)
- [ ] Install: Ultralytics YOLOv8 and run the demo on a sample video

### Day 2 — CCTV analytics specifics
- [ ] Tutorial: YOLOv8 on video stream (webcam or video file)
- [ ] Implement: People counting in a zone
  - Define a polygon region
  - Count entries/exits
  - Report occupancy over time

### Day 3 — Tracking
- [ ] Read: ByteTrack paper (arxiv.org/abs/2110.06864) — simple, effective, widely used
- [ ] Implement: Multi-object tracking on a video using ByteTrack + YOLO
  - Assign consistent IDs across frames
  - Track trajectories

### Day 4 — Edge deployment
- [ ] Read: ONNX Runtime docs → model optimization for edge
- [ ] Convert: YOLOv8 model → ONNX → test inference speed
- [ ] Profile: frames per second on your machine; identify the bottleneck
- [ ] Read: NVIDIA Jetson deployment guide (even if you don't have the hardware — understand the constraints)

### Day 5–6 — Complete pipeline
- [ ] Build: CCTV analytics demo:
  - Input: video file (or webcam)
  - Detect: people, vehicles
  - Track: assign IDs, measure dwell time
  - Alert: if person detected in restricted zone
  - Output: annotated video + JSON event log

### Day 7 — Evidence + publish
- [ ] Polish repo: `cctv-analytics-demo`
- [ ] Record a demo video (the output video IS the evidence)
- [ ] Stub content: "Building a CCTV analytics pipeline from scratch"

---

## Evidence artifact

**Repo**: `cctv-analytics-demo` — person/vehicle detection + tracking + zone alerts
**Demo**: annotated output video (upload to YouTube or include in repo)
**What it proves**: CV + systems + edge thinking — nobody expects a chip designer to also do this

---

## Done criteria

- [ ] Working pipeline on a real video file
- [ ] Tracking with stable IDs across 100+ frames
- [ ] Latency measured and reported in README
- [ ] `profile/my-profile.yaml`: `computer_vision: PROFICIENT, edge_ai: FAMILIAR`
- [ ] `second-brain/learning-log.md`: entry added

---

## Domain opportunities unlocked

After this plan, you can target:
- **Industrial inspection AI** (semiconductor fabs, PCB inspection) — your hardware background is gold
- **Autonomous systems** (ADAS, robotics) — embedded + CV combo
- **Security / surveillance tech** (Avigilon, Genetec, Axis) — in Switzerland and UK
- **Smart city platforms** (EU funding heavy) — in EU/Switzerland

---

## STATUS: TODO

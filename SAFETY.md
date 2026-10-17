# Safety, limitations and pre-deployment checks — DECICE_UC3_Monitor

**Scope:** ROS 2 edge telemetry -> Prometheus metrics in Kubernetes, with a simulated or live data producer.  
**Issued:** 2026-10-17  
**Status:** Risk guidance only. No claim is made that any checklist item is already implemented, tested, legally approved or certified.

This document supplements [DISCLAIMER.md](DISCLAIMER.md) and the existing copyright/license terms without changing either. It does not prevent claims or waive mandatory legal duties.

## Risks to assess

- Bundled example configuration uses generated telemetry; samples must not be misrepresented as live measurements.
- ROS 2 topic changes, exporter stalls, sensor faults and clock drift can yield absent or incorrect metrics.
- An exposed metrics endpoint or insecure Kubernetes manifest can leak operational information.

## Checks before live use

- [ ] Explicitly distinguish simulation from live-data mode on each deployment.
- [ ] Verify source authenticity, freshness, timestamps, units, labels and backpressure under load.
- [ ] Review ingress exposure, authentication, network policies and container privileges.
- [ ] Do not rely on exporter values as a physical-safety or real-time robotics control mechanism.

## User and maintainer responsibilities

Begin in an isolated, authorized test environment; apply least privilege, backups, monitoring and an independent review of any high-impact outputs or actions. Where a project depends on third-party providers or real equipment, comply with vendor terms and safety instructions. Report suspected security flaws privately. Record actual test evidence, versions and unresolved risks rather than inferring that documentation is proof of implementation.

**Mandatory rights preserved:** Liability, product-safety, privacy, security and consumer obligations cannot be eliminated by this notice where applicable law forbids exclusion.

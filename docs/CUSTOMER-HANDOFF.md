# Cisco ACI integration — customer handoff checklist

**Purpose:** Give this page to your customer's **ACI / data-center network** team when scoping a Cisco Secure Workload (CSW) integration with their ACI fabric.

**Integration summary:** CSW's **ACI connector** talks to the **APIC** REST API to (a) import **fabric endpoints and labels** (EPG/BD/VRF context) into CSW inventory, (b) map each **VRF to a CSW scope**, and (c) push **micro-segmentation** into the fabric as **ESG contracts** (programmed into leaf-switch TCAM). It is **two-way**: visibility in, enforcement out.

---

## Integration paths

| Path | What CSW does | Credential needed | Data direction |
|---|---|---|---|
| **Endpoint / label import** | Import endpoints, IPs, EPG/BD/VRF labels | APIC read access | APIC → CSW (HTTPS) |
| **Scope ↔ VRF mapping** | Bind each VRF to one CSW scope | — | CSW config |
| **ESG enforcement** | Push ESG contracts for mapped VRFs | APIC write access (ESG/contracts) | CSW → APIC → fabric TCAM |

---

## What we need from the ACI / network team

### 1. APIC access
| Item | Detail |
|------|--------|
| **APIC nodes** | IP address + port for each APIC node (**max 7**) |
| **Service account** | APIC username/password with rights to read endpoints and write ESG/contract objects for target VRFs (prefer least-privilege over fabric-admin) |
| **Certificate** | Whether the APIC uses a self-signed cert (drives the connector's *Self-signed certificate* checkbox) |
| **Connectivity** | Direct, HTTP proxy (ports 80/8080/443/3128), or Secure Connector tunnel |

### 2. Fabric readiness
| Item | Detail |
|------|--------|
| **VRFs to segment** | List of VRFs to map to CSW scopes (1 VRF → 1 scope) |
| **Micro-segmentation** | "allow micro-segmentation" enabled on the relevant VRF EPG(s) |
| **TCAM headroom** | Confirm leaf switches have sufficient TCAM for the intended contracts |

### 3. Connectivity
| Direction | Source | Destination | Port |
|-----------|--------|-------------|------|
| Outbound | CSW cluster / SaaS Secure Connector VM | Each APIC node | **HTTPS** (443, or proxy 80/8080/443/3128) |
| Outbound (SaaS) | Secure Connector VM | CSW SaaS FQDN | **443/TCP** |

### 4. Facts to confirm
- [ ] APIC node IPs/ports (≤ 7) and reachability from the CSW/Secure Connector source
- [ ] APIC service account + permissions (read endpoints, write ESG/contracts)
- [ ] Self-signed vs CA-signed APIC certificate
- [ ] VRFs → scopes mapping plan (1:1)
- [ ] "allow micro-segmentation" enabled on target VRF EPGs
- [ ] Baseline per-switch TCAM utilization

---

## What CSW will produce

| ACI source | CSW result |
|------------|-----------|
| Fabric endpoints / IPs | Inventory items enriched with ACI context |
| EPG / BD / VRF / tenant | `orchestrator_*` labels for search, scopes, policy |
| Policy intent (mapped VRF) | **ESG contracts** pushed into the fabric (leaf TCAM) |

---

## Security & compliance talking points

- **Least-privilege APIC account** — read endpoints + write ESG/contracts for target VRFs only; avoid full fabric-admin.
- **Single connector per fabric** — recommended to avoid unknown policy interactions.
- **Controlled enforcement** — CSW verifies **TCAM availability** on all participating switches before pushing policy; roll out per VRF/scope.
- **Encrypted** — APIC credentials stored encrypted in CSW; all communication over TLS; use Secure Connector for segmented management networks.
- **Auditable** — imported labels and pushed contracts are versioned and analyzable.

---

## Validation (joint test)

| # | Test | Owner | Pass |
|---|------|-------|------|
| 1 | Connector reaches **all** APIC nodes and shows healthy | Network + CSW | ☐ |
| 2 | Fabric endpoints appear in inventory with `orchestrator_*` labels | CSW admin | ☐ |
| 3 | VRF → scope mapping created (1:1) | CSW admin | ☐ |
| 4 | "allow micro-segmentation" enabled on target VRF EPG | ACI team | ☐ |
| 5 | Policy analysis validates intent before enforcement | Security architect | ☐ |
| 6 | Enforce one VRF → allowed flow works, disallowed flow blocked | ACI + CSW | ☐ |
| 7 | TCAM utilization healthy on all participating leaves post-push | ACI team | ☐ |

---

## Support limitations (share with the customer)

- **Minimum ACI software:** **5.0.1+** for East-West / intra-VRF enforcement; **6.1(4)+** for North-South / L3Out external enforcement. CSW **4.0+**.
- **Allow-list model:** CSW pushes **allow** policies only — **no Deny/Block**, and **catch-all-allow** is not rendered.
- **Not supported:** **Multi-Site** ACI fabrics; **FQDN-** and **process-based** policies; **dual-managed** (CSW- and ACI-owned) policies.
- **Ownership:** once enforcement is on, CSW manages **all** policy for the mapped VRF (even agentless workloads); CSW-created `secureworkload-*` application profiles must not be hand-edited in APIC.
- **No per-rule hit counts** are available from ACI for these policies.

---

## References

- Full guide: [CSW-ACI-Integration-Guide.md](../CSW-ACI-Integration-Guide.md)
- **CSW 4.0 — Secure Workload Integration with ACI (primary):** https://www.cisco.com/c/en/us/td/docs/security/workload_security/secure_workload/user-guide/4_0/cisco-secure-workload-user-guide-on-prem-v40/m-aci-integration-with-secure-workload.html
- Cisco Connectors (ACI): [On-Prem 4.0](https://www.cisco.com/c/en/us/td/docs/security/workload_security/secure_workload/user-guide/4_0/cisco-secure-workload-user-guide-on-prem-v40/configure-and-manage-connectors-for-secure-workload.html)
- Cisco ACI ESG white paper: https://www.cisco.com/c/en/us/solutions/collateral/data-center-virtualization/application-centric-infrastructure/white-paper-c11-743951.html

---

*Generic template — no customer-specific names. Customize APIC endpoints, VRFs, and contacts locally before sending.*

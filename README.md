# Cisco Secure Workload → Cisco ACI Integration Guide

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=chandrapati.csw-aci-integration&left_text=visitors)
[![GitHub stars](https://img.shields.io/github/stars/chandrapati/csw-aci-integration?style=social)](https://github.com/chandrapati/csw-aci-integration/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/chandrapati/csw-aci-integration?style=social)](https://github.com/chandrapati/csw-aci-integration/network/members)
[![Last commit](https://img.shields.io/github/last-commit/chandrapati/csw-aci-integration)](https://github.com/chandrapati/csw-aci-integration/commits/main)

A step-by-step, **beginner-friendly** integration guide for **Cisco ACI** + **Cisco Secure Workload (CSW)** — using the **ACI connector** to import **fabric endpoints & labels** (EPG/BD/VRF), map **VRFs to CSW scopes**, and push **micro-segmentation into the fabric via Endpoint Security Groups (ESGs)** programmed into leaf-switch TCAM.

[![Cisco Secure Workload](https://img.shields.io/badge/Cisco-Secure%20Workload-00205B?logo=cisco&logoColor=white)](https://www.cisco.com/go/secureworkload)
[![Cisco ACI](https://img.shields.io/badge/Cisco-ACI%20%2F%20APIC-0D7377?logo=cisco&logoColor=white)](https://www.cisco.com/c/en/us/support/cloud-systems-management/application-policy-infrastructure-controller-apic/series.html)
[![Enforcement](https://img.shields.io/badge/Enforcement-ESG%20contracts%20(fabric)-2E8B57)](https://www.cisco.com/c/m/en_us/products/security/secure-workload-compatibility-matrix.html)

> **⚠ Disclaimer:** This is a **community reference guide** prepared by Cisco Solutions Engineering — not an official Cisco product document. Always refer to the [official Cisco Secure Workload documentation](https://www.cisco.com/c/en/us/support/security/tetration/series.html), the [Cisco ACI documentation](https://www.cisco.com/c/en/us/support/cloud-systems-management/application-policy-infrastructure-controller-apic/series.html), and the [Compatibility Matrix](https://www.cisco.com/c/m/en_us/products/security/secure-workload-compatibility-matrix.html) for authoritative, up-to-date guidance.

---

## What This Covers

| Area | Detail |
|---|---|
| **Integration type** | ACI **connector** (`type: aci`) — bidirectional |
| **Data imported** | Fabric endpoints/IPs + ACI labels (EPG / BD / VRF / tenant) → `orchestrator_*` |
| **Mapping** | **Scope ↔ VRF** (one VRF → one scope, incl. child scopes) |
| **Enforcement** | ✅ **ESG contracts** pushed to the fabric (programmed into leaf **TCAM**) |
| **Workload coverage** | VMware · Hyper-V · OpenStack · Kubernetes · OpenShift · AWS/Azure/GCP · bare metal |
| **Transport** | HTTPS REST to APIC (self-signed cert supported); proxy ports 80/8080/443/3128 |
| **Scale** | Up to **7 APIC nodes** per connector; **one connector per fabric** recommended |
| **Connectivity** | Direct (on-prem) or via **Secure Connector** tunnel (SaaS / non-routable APIC) |
| **Verified against** | CSW 4.x on-prem and SaaS; Cisco ACI / APIC |

---

## Quick Start

### Prerequisites
- Cisco ACI fabric with reachable **APIC** REST API (HTTPS)
- **APIC service account** (read endpoints + write ESG/contracts for target VRFs)
- APIC node IPs/ports (**≤ 7**)
- Sufficient **leaf TCAM** for intended contracts
- CSW **4.x** with Site Admin / Root Scope Owner rights
- (SaaS / non-routable APIC) a healthy **Secure Connector** tunnel
- Firewall: HTTPS CSW → each APIC (or proxy 80/8080/443/3128)

### Steps (summary)
1. `Manage → Workloads → Connectors → ACI Connector → Configure Your New Connector`.
2. Enter **Name**, **APIC nodes** (≤ 7), **credentials**, self-signed-cert checkbox, connectivity.
3. **Save** → verify endpoints + `orchestrator_*` labels in inventory.
4. **VRF → Scope Mapping** tab → map each VRF (1:1); enable segmentation; tick **"allow micro-segmentation"** on the VRF EPG.
5. Discover + **analyze** policy (no enforcement), then **enforce** → CSW pushes **ESG contracts**.
6. Watch the **Status** tab: CSW checks **TCAM** on all switches before committing.

### Verify
`Investigate → Inventory Search` → confirm ACI endpoints and `orchestrator_*` (EPG/BD/VRF) labels; check the connector **Status** tab for TCAM utilization.

See the [full step-by-step guide](CSW-ACI-Integration-Guide.md) or [open the HTML version](CSW-ACI-Integration-Guide.html).

---

## Architecture Diagram

![CSW and Cisco ACI Integration Architecture](csw-aci-architecture.png)

*The ACI connector imports fabric endpoints and labels from the APIC over HTTPS into CSW inventory; each VRF maps to a CSW scope. On enforcement, CSW translates intent into ESG contracts pushed into the fabric and programmed into leaf-switch TCAM. SaaS / non-routable APICs ride a Secure Connector tunnel.*

---

## Capabilities — at a glance

The ACI connector **extends the cloud connectors and the FMC connector**, and adds:

| Capability | Detail |
|---|---|
| **Fabric visibility** | Workloads / IPs belonging to the ACI fabric |
| **Label ingestion** | ACI labels (EPG / BD / VRF / tenant) as `orchestrator_*` |
| **Scope-to-VRF mapping** | Bind fabric VRFs to CSW scopes for unified policy |
| **ESG enforcement** | Push segmentation into the fabric per-VRF (leaf TCAM) |

---

## Files in This Repo

| File | Description |
|---|---|
| [`README.md`](README.md) | This file — quick start and overview |
| [`CSW-ACI-Integration-Guide.md`](CSW-ACI-Integration-Guide.md) | Full step-by-step guide (Markdown source) |
| [`CSW-ACI-Integration-Guide.html`](CSW-ACI-Integration-Guide.html) | Styled HTML — open in a browser |
| [`csw-aci-architecture.png`](csw-aci-architecture.png) | Architecture diagram |
| [`make_architecture.py`](make_architecture.py) | Regenerate the architecture diagram (requires matplotlib) |
| [`build.sh`](build.sh) | Regenerate HTML/PDF from Markdown (requires pandoc + Chrome) |
| [`examples/aci-connector-openapi.py`](examples/aci-connector-openapi.py) | Reference OpenAPI payload to create the ACI connector (secrets from env) |
| [`examples/vrf-to-scope-mapping-reference.md`](examples/vrf-to-scope-mapping-reference.md) | VRF→scope mapping, micro-seg enablement, ESG rollout, TCAM pre-flight |
| [`docs/CUSTOMER-HANDOFF.md`](docs/CUSTOMER-HANDOFF.md) | Checklist to hand to the customer's ACI / data-center network team |
| [`docs/00-official-references.md`](docs/00-official-references.md) | Authoritative Cisco CSW + ACI/APIC doc links |

---

## Video References

> There is currently **no dedicated CSW + ACI video**. The videos below cover the **connector / label-import** pattern, **scopes**, and **enforcement discipline** this integration builds on. See the guide's [§11](CSW-ACI-Integration-Guide.md#11-video-references).

| Video | Why it's relevant |
|---|---|
| [Connector Overview](https://youtu.be/H6QxuouzeC8) | Connector / label-enrichment pattern |
| [Cisco Secure Workload: Labels](https://www.youtube.com/watch?v=NLoZq0wiTU8) | How imported ACI labels drive policy |
| [Cisco Secure Workload: Scopes](https://www.youtube.com/watch?v=3KBmanCNm4U) | Scope design — relevant to VRF→scope mapping |
| [Production and Test Risk Reduction](https://www.youtube.com/watch?v=HKT18Ylt4IY) | Monitor → enforce discipline before pushing ESG contracts |
| [CSW-User-Education library](https://github.com/chandrapati/CSW-User-Education) | Full curated CSW learning path |

---

## Step-by-Step Guides

Hands-on integration and deployment guides — follow these top to bottom to build out a deployment:

| Guide | Description | Best for |
|-------|-------------|---------|
| [Agent Installation](https://github.com/chandrapati/CSW-Agent-Installation-Guide) | Deploy CSW agents on Linux / Windows / cloud | Day-1 sensor deployment |
| [Kubernetes](https://github.com/chandrapati/csw-kubernetes-integration) | K8s connector + DaemonSet: pod/service labels, flow visibility, iptables enforcement, CVE scanning | Container segmentation (EKS/AKS/GKE/upstream) |
| [OpenShift](https://github.com/chandrapati/csw-openshift-integration) | OpenShift connector + DaemonSet (privileged SCC): project/pod/service labels, flows, iptables enforcement | Red Hat OpenShift segmentation |
| [Policy Lifecycle](https://github.com/chandrapati/CSW-Policy-Lifecycle) | Policy discovery → enforcement workflow | Policy management |
| [vCenter](https://github.com/chandrapati/csw-vcenter-integration) | VMware vCenter VM identity + tag/category label import | Virtualization-driven policy |
| [ACI](https://github.com/chandrapati/csw-aci-integration) | Cisco ACI endpoint/label ingestion, VRF→scope mapping, ESG enforcement | ACI fabric segmentation |
| [DNS](https://github.com/chandrapati/csw-dns-integration) | AXFR zone-transfer hostname labels (`dns_name`) for scopes/policy | Hostname-driven policy |
| [ISE / pxGrid](https://github.com/chandrapati/csw-ise-integration) | ISE/pxGrid: user-identity–aware microsegmentation | Identity & Zero Trust |
| [ServiceNow CMDB](https://github.com/chandrapati/csw-servicenow-integration) | ServiceNow CMDB label enrichment for workload scopes | CMDB-driven policy |
| [Infoblox](https://github.com/chandrapati/csw-infoblox-integration) | Infoblox IPAM/DNS extensible-attribute label enrichment | IPAM/DNS-driven policy |
| [F5 BIG-IP](https://github.com/chandrapati/csw-f5-integration) | F5 virtual-server labels, policy enforcement, IPFIX flow visibility | Load balancer segmentation |
| [NetScaler ADC](https://github.com/chandrapati/csw-netscaler-integration) | NetScaler LB virtual-server labels + ACL policy enforcement | Load balancer segmentation |
| [AWS Connector](https://github.com/chandrapati/csw-aws-connector) | EC2 tag ingestion + VPC flow logs + Security Group enforcement | AWS workloads |
| [Azure Connector](https://github.com/chandrapati/csw-azure-connector) | Azure VM tag ingestion + VNet flow logs + NSG enforcement | Azure workloads |
| [GCP Connector](https://github.com/chandrapati/csw-gcp-connector) | GCE label ingestion + VPC flow logs + firewall enforcement | GCP workloads |
| [NetFlow](https://github.com/chandrapati/csw-netflow-integration) | NetFlow v9/IPFIX agentless flow ingestion from switches | Network fabric visibility |
| [ERSPAN](https://github.com/chandrapati/csw-erspan-integration) | Agentless packet mirroring for legacy / OT / IoT devices | Deep agentless visibility |
| [Secure Firewall](https://github.com/chandrapati/CSW-Secure-Firewall-Integration-Guide) | NSEL flow ingestion + FMC policy enforcement | Firewall visibility & enforcement |
| [Secure Connector](https://github.com/chandrapati/csw-secure-connector) | SaaS reverse-tunnel proxy to private orchestrator APIs (no inbound holes) | SaaS → on-prem reachability |
| [Splunk Integration](https://github.com/chandrapati/csw-splunk-integration) | CSW alerts → Splunk SIEM + all alert notifiers (Email/Slack/PagerDuty/Kinesis/Webex) | SecOps / SIEM teams |

## Resources

Learning paths, reference material, and day-2 tooling:

| Resource | Description | Best for |
|----------|-------------|---------|
| [User Education](https://github.com/chandrapati/CSW-User-Education) | Onboarding guides, concept explainers, and curated video library | New CSW users |
| [Compliance Mapping](https://github.com/chandrapati/CSW-Compliance-Mapping) | Map CSW controls to NIST, PCI-DSS, HIPAA, CIS | Compliance & audit |
| [Tenant Insights](https://github.com/chandrapati/CSW-Tenant-Insights) | Tenant-level reporting and analytics | Visibility metrics |
| [Operations Toolkit](https://github.com/chandrapati/CSW-Operations-Toolkit) | Day-2 ops scripts: health checks, reporting, policy analysis | Ongoing operations |

> **Suggested customer journey:**
> User Education → Agent Installation → ACI → Policy Lifecycle → vCenter → DNS → ISE/pxGrid → ServiceNow CMDB → Compliance Mapping → Operations Toolkit

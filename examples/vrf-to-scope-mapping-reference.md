# VRF → Scope mapping & ESG enforcement reference

This is the step that ties **ACI fabric segmentation** to **CSW policy**. Get the mapping model right *before* you enforce.

---

## 1. The rule: one VRF → one scope

| Principle | Why |
|---|---|
| Map **exactly one VRF to one CSW scope** | Predictable enforcement. All **child scopes** under the mapped scope are considered when policy is enforced. |
| Don't fan multiple VRFs into one scope (or split one VRF across scopes) | Enforcement outcomes become ambiguous and hard to audit. |

**Path:** ACI connector → **VRF to Scope Mapping** tab → **Add mapping**.

```text
ACI VRF                         CSW Scope
-----------------------------   ------------------------------
tenantA:prod-vrf          -->   Default:DC1:Prod
tenantA:nonprod-vrf       -->   Default:DC1:NonProd
tenantB:pci-vrf           -->   Default:DC1:PCI
```

---

## 2. Enable micro-segmentation on the VRF EPG

For ESG-based intra-VRF segmentation to be programmable:

1. In the **VRF to Scope Mapping** tab, **enable segmentation** for the mapped VRF.
2. Edit the **VRF EPG** and tick **"allow micro-segmentation"**.

Without this, CSW can import/visualize but cannot push ESG contracts for that VRF.

---

## 3. Enforcement flow (safe rollout)

```text
1. Import endpoints/labels        (connector healthy)
2. Map VRF -> scope               (1:1)
3. Enable segmentation on VRF     (+ allow micro-segmentation on VRF EPG)
4. Policy discovery + live analysis   (NO enforcement yet)
5. Enforce scope  -> CSW pushes ESG contracts to the fabric
6. CSW checks TCAM on all participating switches BEFORE committing
7. Validate allowed vs denied flows; roll out VRF by VRF
```

---

## 4. TCAM pre-flight (Status tab)

The connector **Status** tab shows **per-switch TCAM utilization**. CSW pushes policy only when **all participating switches have sufficient TCAM**.

| Check | Action |
|---|---|
| Enforcement doesn't complete | A leaf is low on TCAM — free space / reduce contracts / stagger rollout |
| Policy on some switches only | Uneven TCAM — review per-switch utilization before re-pushing |

> Review TCAM headroom **before** large policy pushes. Insufficient TCAM blocks or partially applies enforcement.

---

## 5. Agents vs. fabric enforcement

The ACI connector realizes segmentation **agentlessly** as **fabric ESG contracts** (leaf TCAM). For workloads in an **ACI-enforced VRF**, keep the **agent profile enforcement set to *Disabled*** — the fabric enforces, not the host — to avoid double-enforcement. The agents are still valuable: they supply the **telemetry** that drives AI policy discovery.

| Workload / tier | Enforcement point |
|---|---|
| In an ACI-enforced VRF (mapped + segmentation on) | **Fabric** (ACI ESG contracts); agent enforcement **Disabled** |
| Not enforced via the fabric | **Host** (CSW agent) where installed |

> **Dual-management** of the same VRF (CSW-owned **and** ACI-owned policies) is **not supported** — let CSW own the mapped VRF's policy end to end. CSW-created `secureworkload-*` application profiles on APIC must not be hand-edited.

#!/usr/bin/env python3
"""Render the CSW <-> Cisco ACI integration architecture diagram.

Produces ``csw-aci-architecture.png`` in the same visual language as the other
connector guides (Kubernetes, vCenter, DNS): Cisco navy/blue palette, rounded
panels, labelled data-flow arrows, real vector text.

The ACI integration is **two-way**: the ACI connector imports fabric endpoints
and labels from APIC INTO CSW (inventory enrichment + Scope-to-ACI/VRF
mapping), and CSW can push segmentation DOWN into the fabric via Endpoint
Security Groups (ESGs), which are programmed into leaf-switch TCAM.

Run:  python3 make_architecture.py
Requires: matplotlib
"""
import math
from matplotlib import pyplot as plt
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Circle,
                                Rectangle, Ellipse, Arc)

# ---- Cisco / ACI palette ----------------------------------------------------
NAVY = "#00205B"
BLUE = "#007BC7"
CYAN = "#00BCEB"
ACI = "#0D7377"       # ACI teal
ACI_D = "#095457"
INK = "#1A1A2E"
GREY = "#555555"
LIGHT = "#F5F8FC"
ACIBG = "#E6F3F3"
BLUEBG = "#EAF4FB"
GREEN = "#2E8B57"
AMBER = "#B5772C"

fig, ax = plt.subplots(figsize=(13.4, 8.4), dpi=100)
ax.set_xlim(0, 134)
ax.set_ylim(0, 84)
ax.axis("off")


def panel(x, y, w, h, edge, fc="white", lw=2.2, rounding=1.4, z=1, ls="solid"):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={rounding}",
        linewidth=lw, edgecolor=edge, facecolor=fc, zorder=z, linestyle=ls))


def box(x, y, w, h, edge, fc="white", lw=1.4, rounding=0.9, z=2, ls="solid"):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={rounding}",
        linewidth=lw, edgecolor=edge, facecolor=fc, zorder=z, linestyle=ls))


def text(x, y, s, size=11, color=INK, weight="normal", ha="center", va="center", z=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=z,
            fontfamily=["Helvetica Neue", "Arial", "DejaVu Sans"])


def switch(cx, cy, w, h, color, label):
    """A simple network-switch glyph."""
    box(cx - w / 2, cy - h / 2, w, h, color, "white", lw=1.5, rounding=0.5)
    # little port ticks
    for i in range(4):
        px = cx - w / 2 + 1.4 + i * (w - 2.8) / 3
        ax.add_patch(Rectangle((px, cy - h / 2 + 0.8), 0.7, 0.7,
                     facecolor=color, edgecolor="none", zorder=4))
    text(cx, cy + 0.7, label, size=8.0, color=color, weight="bold")


# ---- Title + Cisco wordmark -------------------------------------------------
text(60, 80, "Cisco Secure Workload  \u2013  Cisco ACI Integration",
     size=21, color=NAVY, weight="bold")

lx = 118.0
heights = [1.6, 2.6, 3.6, 2.6, 1.6, 2.6, 3.6, 4.6, 3.6, 2.6, 1.6]
for i, hh in enumerate(heights):
    ax.add_patch(Rectangle((lx + i * 0.75, 79.0 - hh / 2), 0.32, hh,
                 facecolor=NAVY, edgecolor="none", zorder=5))
text(lx + len(heights) * 0.375, 74.9, "CISCO", size=10, color=NAVY, weight="bold")

# =============================================================================
# LEFT PANEL  --  Cisco Secure Workload
# =============================================================================
panel(3, 16, 40, 56, BLUE)
text(23, 68.4, "Cisco Secure Workload", size=14, color=BLUE, weight="bold")
text(23, 65.4, "(SaaS tenant or on-prem cluster)", size=9, color=GREY)

# ACI connector box
box(6, 58.0, 34, 5.8, BLUE, BLUEBG)
ax.add_patch(Circle((9.8, 60.9), 1.5, facecolor=BLUE, edgecolor="white", lw=0.8, zorder=4))
ax.add_patch(Circle((9.8, 60.9), 0.55, facecolor="white", zorder=5))
text(25, 61.6, "ACI Connector", size=9.6, color=NAVY, weight="bold")
text(25, 59.6, "Manage \u2192 Workloads \u2192 Connectors", size=7.8, color=GREY)

# inventory cylinder
cx, cy, cw, ch = 8.0, 47.5, 12, 7.5
ax.add_patch(Rectangle((cx, cy), cw, ch, facecolor="white", edgecolor=NAVY, lw=1.7, zorder=3))
ax.add_patch(Ellipse((cx + cw / 2, cy + ch), cw, 2.0, facecolor="white", edgecolor=NAVY, lw=1.7, zorder=4))
ax.add_patch(Ellipse((cx + cw / 2, cy), cw, 2.0, facecolor="white", edgecolor=NAVY, lw=1.7, zorder=3))
text(cx + cw / 2, cy + ch / 2 + 0.4, "Inventory", size=9, color=NAVY, weight="bold")
text(cx + cw / 2, cy + ch / 2 - 1.6, "(endpoints)", size=8, color=NAVY)
text(31, 51.6, "orchestrator_*", size=8, color=GREY)
text(31, 49.8, "ACI labels /", size=8, color=GREY)
text(31, 48.0, "EPG \u00b7 BD \u00b7 VRF", size=8, color=GREY)

# scope-to-VRF mapping pill
box(6, 39.0, 34, 6.4, ACI, ACIBG)
text(23, 43.2, "Scope \u2194 VRF mapping", size=9.0, color=ACI_D, weight="bold")
text(23, 41.1, "one VRF \u2192 one scope (+ child scopes)", size=7.7, color=GREY)

# scopes + policies pills
box(6, 31.0, 15, 5.2, BLUE, BLUE)
text(13.5, 33.6, "Scopes", size=9.3, color="white", weight="bold")
box(25, 31.0, 15, 5.2, NAVY, NAVY)
text(32.5, 33.6, "Policies", size=9.3, color="white", weight="bold")

# ESG enforcement note
box(6, 22.5, 34, 6.6, GREEN, "#EAF6EF")
text(23, 26.9, "Segmentation \u2192 ESG contracts", size=8.7, color=GREEN, weight="bold")
text(23, 24.9, "pushed to fabric (per-VRF micro-seg)", size=8.0, color=GREY)

# =============================================================================
# RIGHT PANEL  --  Cisco ACI fabric
# =============================================================================
panel(58, 12, 73, 60, ACI)
text(94.5, 68.6, "Cisco ACI Fabric", size=14, color=ACI_D, weight="bold")
text(94.5, 65.8, "APIC controllers + spine/leaf + endpoints", size=9, color=GREY)

# APIC cluster box
box(61, 58.5, 30, 5.8, ACI_D, ACIBG)
ax.add_patch(Circle((64.6, 61.4), 1.6, facecolor=ACI, edgecolor="white", lw=0.8, zorder=4))
text(64.6, 61.4, "API", size=6.2, color="white", weight="bold", z=6)
text(79.5, 62.3, "APIC controllers (up to 7)", size=9.2, color=ACI_D, weight="bold")
text(79.5, 60.2, "REST API \u00b7 admin creds \u00b7 HTTPS", size=7.8, color=GREY)

# ESG / EPG catalog box (top-right)
box(98, 58.5, 30, 5.8, GREEN, "#EAF6EF")
text(113, 62.3, "ESG / EPG / Contracts", size=9.2, color=GREEN, weight="bold")
text(113, 60.2, "endpoint security groups", size=7.8, color=GREY)

# spine switches
switch(74, 51.5, 12, 4.6, ACI, "Spine")
switch(94, 51.5, 12, 4.6, ACI, "Spine")
# leaf switches
switch(68, 43.5, 11, 4.4, ACI_D, "Leaf")
switch(83, 43.5, 11, 4.4, ACI_D, "Leaf")
switch(98, 43.5, 11, 4.4, ACI_D, "Leaf")
switch(115, 43.5, 11, 4.4, ACI_D, "Leaf")
# spine-leaf mesh lines
for sx in (74, 94):
    for lx2 in (68, 83, 98, 115):
        ax.plot([sx, lx2], [51.5 - 2.3, 43.5 + 2.2], color=ACI, lw=0.6, alpha=0.5, zorder=2)

# TCAM strip
box(61, 36.0, 67, 5.2, AMBER, "#F7EFE4")
text(94.5, 39.4, "Leaf-switch TCAM  \u2014  contracts programmed here", size=8.6, color=AMBER, weight="bold")
text(94.5, 37.3, "enforcement checks TCAM availability on all switches before pushing policy", size=7.6, color=GREY)

# endpoints strip (workloads)
box(61, 24.5, 67, 9.6, ACI, "white", lw=1.6)
text(94.5, 32.6, "Endpoints (any location / any hypervisor / any cloud)", size=8.8, color=ACI_D, weight="bold")
labels = ["VMware", "Hyper-V", "OpenStack", "K8s /\nOpenShift", "AWS /\nAzure /\nGCP", "bare\nmetal"]
ew = 67 / len(labels)
for i, lb in enumerate(labels):
    ex = 61 + 1.2 + i * ew
    box(ex, 25.4, ew - 2.4, 4.6, ACI, ACIBG, lw=1.0, rounding=0.5)
    text(ex + (ew - 2.4) / 2, 27.7, lb, size=6.8, color=ACI_D, weight="bold")

# =============================================================================
# CONNECTING ARROWS
# =============================================================================
# 1. Import endpoints + labels IN (APIC -> CSW) HTTPS
ax.add_patch(FancyArrowPatch((61, 61.0), (40.5, 60.9),
             arrowstyle="-|>", mutation_scale=22, linewidth=3.0, color=BLUE, zorder=6))
text(50.3, 63.0, "HTTPS REST", size=8.4, color=BLUE, weight="bold")
text(50.3, 61.2, "import endpoints", size=7.4, color=GREY)

# 2. Enforcement pushed DOWN (CSW -> APIC -> ESG) 
ax.add_patch(FancyArrowPatch((40.5, 25.8), (61, 29.0),
             arrowstyle="-|>", mutation_scale=20, linewidth=2.6, color=GREEN, zorder=6))
text(50, 24.2, "ESG contracts", size=8.2, color=GREEN, weight="bold")
text(50, 22.4, "push segmentation", size=7.4, color=GREY)

# =============================================================================
# Secure Connector tunnel note (bottom-left, dashed)
# =============================================================================
box(3, 8.0, 40, 5.6, BLUE, "white", lw=1.5, ls=(0, (4, 3)))
ax.add_patch(Arc((7.2, 11.4), 1.5, 1.7, theta1=0, theta2=180,
             linewidth=1.4, edgecolor=BLUE, zorder=6))
ax.add_patch(FancyBboxPatch((6.15, 9.1), 2.1, 1.9,
             boxstyle="round,pad=0,rounding_size=0.25",
             facecolor=BLUE, edgecolor="none", zorder=6))
ax.add_patch(Circle((7.2, 10.0), 0.3, facecolor="white", zorder=7))
text(26, 11.5, "Secure Connector tunnel", size=8.6, color=NAVY, weight="bold")
text(26, 9.5, "(SaaS / non-routable APIC) \u00b7 proxy ports 80/8080/443/3128", size=7.3, color=GREY)

# right-side note
box(58, 8.0, 73, 5.6, ACI, ACIBG, lw=1.5)
text(94.5, 11.5, "One connector per fabric (recommended) \u00b7 up to 7 APIC nodes", size=8.4, color=ACI_D, weight="bold")
text(94.5, 9.5, "Status tab shows per-switch TCAM utilization before/after enforcement", size=7.5, color=GREY)

# ---- bottom gradient bar ----------------------------------------------------
grad_y = 2.0
for i in range(200):
    frac = i / 199
    if frac < 0.6:
        t = frac / 0.6
        r = int(0x00); g = int(0x20 + t * (0x7b - 0x20)); b = int(0x5b + t * (0xc7 - 0x5b))
    else:
        t = (frac - 0.6) / 0.4
        r = int(0x00); g = int(0x7b + t * (0xbc - 0x7b)); b = int(0xc7 + t * (0xeb - 0xc7))
    ax.add_patch(Rectangle((3 + frac * 128, grad_y), 128 / 200 + 0.2, 0.9,
                 facecolor=f"#{r:02x}{g:02x}{b:02x}", edgecolor="none", zorder=2))

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
out = "csw-aci-architecture.png"
plt.savefig(out, dpi=100, facecolor="white", bbox_inches="tight", pad_inches=0.15)
print("wrote", out)

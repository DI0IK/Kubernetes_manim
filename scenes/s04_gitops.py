from manim import *
from manim_slides import Slide
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY, GIT_ORANGE
)
from helpers import create_modern_box


class GitopsCLI(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("GitOps vs. CLI", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Moderne Deployment-Strategien im Vergleich", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        self.play(FadeIn(title, shift=UP*0.2), FadeIn(subtitle, shift=UP*0.2))
        self.next_slide()
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Klassisches Tooling
        # ==========================================
        t2 = Text("Klassisches Tooling", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        # kubectl Box mit "Card" Design (Titel innenliegend)
        kubectl_panel = RoundedRectangle(width=4.5, height=3.2, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_color=K8S_BLUE, fill_opacity=0.05)
        kubectl_title = Text("kubectl", font_size=24, color=K8S_BLUE, weight=BOLD).align_to(kubectl_panel, UL).shift(RIGHT*0.4 + DOWN*0.4)
        kubectl_sub = Text("Imperativ / CLI", font_size=18, color=TEXT_MUTED).next_to(kubectl_title, DOWN, buff=0.1).align_to(kubectl_title, LEFT)
        
        cmds = VGroup(
            Text("kubectl apply -f deploy.yml", font_size=18, color=STORE_YELLOW, font="Monospace"),
            Text("kubectl get pods -w", font_size=18, color=STORE_YELLOW, font="Monospace"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(kubectl_sub, DOWN, buff=0.5).align_to(kubectl_title, LEFT)
        
        kubectl_group = VGroup(kubectl_panel, kubectl_title, kubectl_sub, cmds).shift(LEFT*3.5 + DOWN*0.2)

        # k9s Box (Terminal UI)
        k9s_panel = RoundedRectangle(width=4.5, height=3.2, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_color=NODE_GREEN, fill_opacity=0.05)
        k9s_title = Text("k9s", font_size=24, color=NODE_GREEN, weight=BOLD).align_to(k9s_panel, UL).shift(RIGHT*0.4 + DOWN*0.4)
        k9s_sub = Text("Terminal-UI (TUI)", font_size=18, color=TEXT_MUTED).next_to(k9s_title, DOWN, buff=0.1).align_to(k9s_title, LEFT)
        
        k9s_desc = Text("Schnelle Cluster-Navigation\n& Live-Metriken", font_size=18, color=TEXT_LIGHT, line_spacing=1.5).next_to(k9s_sub, DOWN, buff=0.6).align_to(k9s_title, LEFT)
        
        k9s_group = VGroup(k9s_panel, k9s_title, k9s_sub, k9s_desc).shift(RIGHT*3.5 + DOWN*0.2)

        # Purposeful staggered animation
        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(kubectl_panel), Write(kubectl_title), FadeIn(kubectl_sub)),
                AnimationGroup(DrawBorderThenFill(k9s_panel), Write(k9s_title), FadeIn(k9s_sub)),
                lag_ratio=0.3
            )
        )
        self.play(FadeIn(k9s_desc, shift=UP*0.2))

        # Schreibmaschinen-Effekt für die Terminal Commands
        for cmd in cmds:
            self.play(AddTextLetterByLetter(cmd), run_time=0.8)
        self.next_slide()

        # ==========================================
        # SLIDE 3: GitOps Paradigma
        # ==========================================
        self.play(FadeOut(kubectl_group), FadeOut(k9s_group))
        
        t3 = Text("GitOps Paradigma", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        # Die architektonisch korrekte Kette (mit größerem Buff, damit Arrows Platz haben)
        git = create_modern_box("Git\nRepository", width=2.8, height=1.5, color=GIT_ORANGE)
        agent = create_modern_box("GitOps\nAgent", width=2.8, height=1.5, color=K8S_BLUE)
        cluster = create_modern_box("Kubernetes\nCluster", width=2.8, height=1.5, color=NODE_GREEN)
        
        flow_group = VGroup(git, agent, cluster).arrange(RIGHT, buff=1.8).move_to(ORIGIN + DOWN*0.2)

        self.play(DrawBorderThenFill(git[0]), Write(git[1]))
        self.play(DrawBorderThenFill(agent[0]), Write(agent[1]))

        # Pull/Watch Pfeil (Datenfluss Git -> Agent)
        pull_arrow = Arrow(git.get_right(), agent.get_left(), color=TEXT_MUTED, buff=0.1).set_z_index(-1)
        pull_label = Text("1. Watch / Pull", font_size=14, color=TEXT_LIGHT, weight=BOLD).next_to(pull_arrow, UP, buff=0.15)
        
        self.play(GrowArrow(pull_arrow), FadeIn(pull_label, shift=UP*0.2))
        
        # Sync Pfeil (Agent wendet Änderungen auf Cluster an)
        self.play(DrawBorderThenFill(cluster[0]), Write(cluster[1]))
        
        sync_arrow = Arrow(agent.get_right(), cluster.get_left(), color=TEXT_MUTED, buff=0.1).set_z_index(-1)
        sync_label = Text("2. Sync / Apply", font_size=14, color=TEXT_LIGHT, weight=BOLD).next_to(sync_arrow, UP, buff=0.15)
        
        self.play(GrowArrow(sync_arrow), FadeIn(sync_label, shift=UP*0.2))

        gitops_group = VGroup(flow_group, pull_arrow, pull_label, sync_arrow, sync_label)
        self.next_slide()

        # ==========================================
        # SLIDE 4: ArgoCD vs Flux
        # ==========================================
        self.play(FadeOut(gitops_group))
        
        t4 = Text("ArgoCD & Flux", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4))

        # ArgoCD Visuell aufwerten (Als Card mit Header)
        argo_base = RoundedRectangle(width=4.5, height=3.2, corner_radius=0.2, color=STORE_YELLOW, stroke_width=2, fill_color=STORE_YELLOW, fill_opacity=0.05)
        argo_title = Text("ArgoCD", font_size=24, color=STORE_YELLOW, weight=BOLD).align_to(argo_base, UL).shift(RIGHT*0.4 + DOWN*0.4)
        
        argo_desc = Text("Fokus auf Web-UI &\nVisuelles Dashboard", font_size=18, color=TEXT_LIGHT, line_spacing=1.2).next_to(argo_title, DOWN, buff=0.5).align_to(argo_title, LEFT)
        
        argocd_g = VGroup(argo_base, argo_title, argo_desc).shift(LEFT*3.5 + DOWN*0.2)

        # Flux Visuell aufwerten (Als Card mit Header)
        flux_base = RoundedRectangle(width=4.5, height=3.2, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_color=K8S_BLUE, fill_opacity=0.05)
        flux_title = Text("Flux", font_size=24, color=K8S_BLUE, weight=BOLD).align_to(flux_base, UL).shift(RIGHT*0.4 + DOWN*0.4)
        
        flux_desc = Text("K8s-nativ via CRDs\nDeklarativer Ansatz", font_size=18, color=TEXT_LIGHT, line_spacing=1.2).next_to(flux_title, DOWN, buff=0.5).align_to(flux_title, LEFT)
        
        flux_g = VGroup(flux_base, flux_title, flux_desc).shift(RIGHT*3.5 + DOWN*0.2)

        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(argo_base), Write(argo_title), FadeIn(argo_desc, shift=UP*0.2)),
                AnimationGroup(DrawBorderThenFill(flux_base), Write(flux_title), FadeIn(flux_desc, shift=UP*0.2)),
                lag_ratio=0.3
            )
        )
        self.next_slide()

        # ==========================================
        # SLIDE 5: Helm & Kustomize
        # ==========================================
        self.play(FadeOut(argocd_g), FadeOut(flux_g))

        t5 = Text("Helm & Kustomize", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t5))

        helm_base = RoundedRectangle(width=4.5, height=3.2, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_color=K8S_BLUE, fill_opacity=0.05)
        helm_title = Text("Helm", font_size=24, color=K8S_BLUE, weight=BOLD).align_to(helm_base, UL).shift(RIGHT*0.4 + DOWN*0.4)
        helm_sub = Text("Package Manager", font_size=16, color=TEXT_MUTED).next_to(helm_title, DOWN, buff=0.1).align_to(helm_title, LEFT)
        helm_items = VGroup(
            Text("• Charts & Templates", font_size=16, color=TEXT_LIGHT),
            Text("• Versionierte Pakete", font_size=16, color=TEXT_LIGHT),
            Text("• Einfaches Deployment", font_size=16, color=TEXT_LIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(helm_sub, DOWN, buff=0.5).align_to(helm_title, LEFT)
        helm_g = VGroup(helm_base, helm_title, helm_sub, helm_items).shift(LEFT*3.5 + DOWN*0.2)

        kust_base = RoundedRectangle(width=4.5, height=3.2, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_color=NODE_GREEN, fill_opacity=0.05)
        kust_title = Text("Kustomize", font_size=24, color=NODE_GREEN, weight=BOLD).align_to(kust_base, UL).shift(RIGHT*0.4 + DOWN*0.4)
        kust_sub = Text("YAML-Overlays", font_size=16, color=TEXT_MUTED).next_to(kust_title, DOWN, buff=0.1).align_to(kust_title, LEFT)
        kust_items = VGroup(
            Text("• base / overlays Struktur", font_size=16, color=TEXT_LIGHT),
            Text("• Umgebungsspezifische Patches", font_size=16, color=TEXT_LIGHT),
            Text("• Kein Template-System", font_size=16, color=TEXT_LIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(kust_sub, DOWN, buff=0.5).align_to(kust_title, LEFT)
        kust_g = VGroup(kust_base, kust_title, kust_sub, kust_items).shift(RIGHT*3.5 + DOWN*0.2)

        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(helm_base), Write(helm_title), FadeIn(helm_sub), FadeIn(helm_items, shift=UP*0.1)),
                AnimationGroup(DrawBorderThenFill(kust_base), Write(kust_title), FadeIn(kust_sub), FadeIn(kust_items, shift=UP*0.1)),
                lag_ratio=0.3
            )
        )
        self.next_slide()

        # ==========================================
        # SLIDE 6: Outro
        # ==========================================
        outro = Text("GitOps = Deployments mit Sicherheitsnetz", font_size=BODY_SIZE + 4, color=NODE_GREEN, weight=BOLD)
        
        self.play(FadeOut(helm_g), FadeOut(kust_g), Transform(title, outro))
        self.play(title.animate.center().scale(1.1))
        self.next_slide()
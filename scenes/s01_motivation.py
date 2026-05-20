from manim import *
from manim_slides import Slide
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY
)
from helpers import create_modern_box, create_uniform_arrow

def create_modern_stack(layers, colors, widths, heights):
    stack = VGroup()
    for name, col, w, h in zip(layers, colors, widths, heights):
        rect = RoundedRectangle(
            corner_radius=0.15, width=w, height=h, color=col, 
            stroke_width=2, fill_color=col, fill_opacity=BG_BOX_OPACITY
        )
        text = Text(name, font_size=18, color=TEXT_LIGHT, weight=BOLD)
        stack.add(VGroup(rect, text.move_to(rect.get_center())))
    stack.arrange(DOWN, buff=0.1)
    return stack

class GeschichteMotivation(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("Geschichte & Motivation", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Warum Kubernetes?", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        self.play(Write(title, run_time=1.5), FadeIn(subtitle, shift=UP*0.5, run_time=1.5))
        self.next_slide(notes="**Monolith** – Eine einzelne, große Codebasis. Probleme: Langsame Releases, Skalierung nur als Ganzes, hohe Fehlerabhängigkeit.")
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Das Problem vor Kubernetes
        # ==========================================
        t2 = Text("Das Problem vor Kubernetes", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        # Monolith als VGroup mit modernem Styling
        monolith_rect = RoundedRectangle(corner_radius=0.2, width=5, height=3, color=CTRL_RED, fill_color=CTRL_RED, fill_opacity=0.2, stroke_width=3)
        ml_text = Text("Monolith", font_size=32, color=TEXT_LIGHT, weight=BOLD).move_to(monolith_rect)
        monolith = VGroup(monolith_rect, ml_text)
        
        self.play(DrawBorderThenFill(monolith_rect), Write(ml_text))
        self.next_slide(notes="**VM vs Container** – VMs enthalten ein eigenes Betriebssystem (Guest OS) + Hypervisor, das macht sie schwer (~GB). Container teilen sich den Host-Kernel und sind daher leicht (~MB).")

        # Risse im Monolithen
        cracks = VGroup(
            Line(monolith_rect.get_corner(UL) + RIGHT*0.8, monolith_rect.get_center() + UP*0.3, color=CTRL_RED, stroke_width=4),
            Line(monolith_rect.get_center() + UP*0.3, monolith_rect.get_corner(DR) + LEFT*0.8, color=CTRL_RED, stroke_width=4),
            Line(monolith_rect.get_corner(UR) + LEFT*0.8, monolith_rect.get_center() + DOWN*0.2, color=CTRL_RED, stroke_width=4),
            Line(monolith_rect.get_center() + DOWN*0.2, monolith_rect.get_corner(DL) + RIGHT*0.5, color=CTRL_RED, stroke_width=4),
        )
        self.play(Create(cracks), run_time=0.8)

        # Beben-Effekt (durch rate_func=sinus schwingt es vor und zurück)
        self.play(
            monolith.animate.shift(RIGHT*0.1),
            cracks.animate.shift(RIGHT*0.1),
            rate_func=lambda t: np.sin(t * 8 * np.pi),
            run_time=0.8,
        )

        # Bruchstücke definieren
        offsets = [
            UP * 0.75 + LEFT * 1.25,   # Oben Links
            UP * 0.75 + RIGHT * 1.25,  # Oben Rechts
            DOWN * 0.75 + LEFT * 1.25, # Unten Links
            DOWN * 0.75 + RIGHT * 1.25 # Unten Rechts
        ]

        pieces = VGroup()
        for off in offsets:
            p = RoundedRectangle(corner_radius=0.1, width=2.5, height=1.5, color=CTRL_RED, fill_color=CTRL_RED, fill_opacity=0.2)
            p.move_to(monolith_rect.get_center() + off)
            pieces.add(p)

        # Nahtloser Austausch (Bruchstücke ersetzen den gezeichneten Monolithen)
        self.add(pieces)
        self.remove(monolith, cracks)

        # Explosionsanimation
        directions = [LEFT*3+UP*2, RIGHT*3+UP*2, LEFT*3+DOWN*2, RIGHT*3+DOWN*2]
        rotations = [PI/4, -PI/4, -PI/6, PI/6]
        
        # Bruchstücke fliegen weg und verblassen
        anims = [
            p.animate.shift(d).rotate(r).set_opacity(0)
            for p, d, r in zip(pieces, directions, rotations)
        ]
        self.play(LaggedStart(*anims, lag_ratio=0.1, run_time=1.2))

        # ==========================================
        # SLIDE 3: Container Orchestrierung
        # ==========================================
        t3 = Text("Container: Leicht & Schnell", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        # VM Stack bauen
        vm_layers = ["App A", "Bins/Libs", "Guest OS", "Hypervisor"]
        vm_colors = [K8S_BLUE, K8S_BLUE, CTRL_RED, BOX_GRAY]
        vm_sizes = [(2.8, 0.8), (2.8, 0.8), (2.8, 1.2), (2.8, 0.6)]
        vm_stack = create_modern_stack(vm_layers, vm_colors, [s[0] for s in vm_sizes], [s[1] for s in vm_sizes])

        vm_box = RoundedRectangle(corner_radius=0.2, width=3.4, height=4.2, color=BOX_GRAY, stroke_width=2, fill_opacity=0.05)
        vm_title = Text("Virtual Machine", font_size=20, color=TEXT_LIGHT, weight=BOLD).next_to(vm_box, UP, buff=0.2)
        vm_group = VGroup(vm_title, vm_box, vm_stack.move_to(vm_box.get_center())).shift(LEFT*3.5 + DOWN*0.2)
        vm_text = Text("Schwergewichtig", font_size=18, color=CTRL_RED, weight=BOLD).next_to(vm_group, DOWN, buff=0.3)

        self.play(DrawBorderThenFill(vm_box), Write(vm_title))
        self.play(LaggedStart(*[FadeIn(layer, shift=UP*0.2) for layer in reversed(vm_stack)], lag_ratio=0.2))
        self.play(FadeIn(vm_text, shift=UP*0.2))
        self.next_slide(notes="Container teilen sich den Host-Kernel → kein eigener Overhead. Start in Sekunden statt Minuten. Ideal für Microservices.")

        ctr_layers = ["App A", "Bins/Libs", "Container Engine"]
        ctr_colors = [NODE_GREEN, NODE_GREEN, STORE_YELLOW]
        ctr_sizes = [(2.8, 0.8), (2.8, 0.8), (2.8, 0.6)]
        ctr_stack = create_modern_stack(ctr_layers, ctr_colors, [s[0] for s in ctr_sizes], [s[1] for s in ctr_sizes])

        ctr_box = RoundedRectangle(corner_radius=0.2, width=3.4, height=2.8, color=NODE_GREEN, stroke_width=2, fill_opacity=0.05)
        ctr_title = Text("Container", font_size=20, color=TEXT_LIGHT, weight=BOLD).next_to(ctr_box, UP, buff=0.2)
        
        # An der VM ausrichten, damit der Größenunterschied visuell wirkt
        ctr_group = VGroup(ctr_title, ctr_box, ctr_stack.move_to(ctr_box.get_center()))
        ctr_group.shift(RIGHT*3.5).align_to(vm_group, DOWN)
        ctr_text = Text("Leichtgewichtig", font_size=18, color=NODE_GREEN, weight=BOLD).next_to(ctr_group, DOWN, buff=0.3)

        self.play(DrawBorderThenFill(ctr_box), Write(ctr_title))
        self.play(LaggedStart(*[FadeIn(layer, shift=UP*0.2) for layer in reversed(ctr_stack)], lag_ratio=0.2))
        self.play(FadeIn(ctr_text, shift=UP*0.2))
        self.next_slide(notes="**Zeitleiste** – Google Borg (~2003): interner Cluster-Manager. Kubernetes 1.0 (2015): Open-Source-Release. CNCF Graduation (2018): K8s wird reif erklärt. **CNCF** = Cloud Native Computing Foundation.")

        self.play(
            FadeOut(vm_group), FadeOut(vm_text), 
            FadeOut(ctr_group), FadeOut(ctr_text)
        )
        
        # ==========================================
        # SLIDE 4: Ursprung und Geschichte
        # ==========================================
        t4 = Text("Ursprung: Von Google zur CNCF", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4))

        borg = create_modern_box("Google\nBorg", width=2.5, height=1.5, color=BOX_GRAY).shift(LEFT*3.5)
        k8s = create_modern_box("Kubernetes\n1.0", width=2.5, height=1.5, color=K8S_BLUE)
        cncf = create_modern_box("CNCF\nGraduated", width=2.5, height=1.5, color=NODE_GREEN).shift(RIGHT*3.5)

        year1 = Text("~2003", font_size=SMALL_SIZE, color=TEXT_MUTED, weight=BOLD).next_to(borg, DOWN, buff=0.3)
        year2 = Text("2015", font_size=SMALL_SIZE, color=K8S_BLUE, weight=BOLD).next_to(k8s, DOWN, buff=0.3)
        year3 = Text("2018", font_size=SMALL_SIZE, color=NODE_GREEN, weight=BOLD).next_to(cncf, DOWN, buff=0.3)

        arrow1 = create_uniform_arrow(borg.get_right(), k8s.get_left())
        arrow2 = create_uniform_arrow(k8s.get_right(), cncf.get_left())

        # Stufenweises Einblenden der Timeline
        self.play(DrawBorderThenFill(borg[0]), Write(borg[1]), FadeIn(year1, shift=UP*0.2))
        self.play(GrowArrow(arrow1))
        
        self.play(DrawBorderThenFill(k8s[0]), Write(k8s[1]), FadeIn(year2, shift=UP*0.2))
        self.play(GrowArrow(arrow2))
        
        self.play(DrawBorderThenFill(cncf[0]), Write(cncf[1]), FadeIn(year3, shift=UP*0.2))
        self.next_slide(notes="**Fazit** – Kubernetes ist der De-facto-Standard für Container-Orchestrierung. Alle großen Cloud-Provider bieten Managed K8s an.")

        # ==========================================
        out_text1 = Text("Kubernetes ist der De-facto-Standard", font_size=BODY_SIZE + 4, color=TEXT_MUTED)
        out_text2 = Text("für Container-Orchestrierung", font_size=BODY_SIZE + 4, color=NODE_GREEN, weight=BOLD)
        out_text = VGroup(out_text1, out_text2).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        # Alles auf einmal ausblenden und den Titel geschmeidig zum Fazit in der Mitte morphen
        self.play(
            *[FadeOut(m) for m in self.mobjects if m != title],
            run_time=1.0
        )
        self.play(Transform(title, out_text))
        self.wait(1)
        self.next_slide()

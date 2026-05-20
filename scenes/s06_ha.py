from manim import *
from manim_slides import Slide
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY
)
from helpers import create_modern_box, create_uniform_arrow


class HighAvailability(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("High Availability (HA)", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Ausfallsicherheit auf allen Ebenen", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        self.play(FadeIn(title, shift=UP*0.2), FadeIn(subtitle, shift=UP*0.2))
        self.next_slide()
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Ausfallsicherheit auf Anwendungsebene
        # ==========================================
        t2 = Text("Ausfallsicherheit auf Anwendungsebene", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        # Rahmen für das ReplicaSet
        rs_box = RoundedRectangle(width=8, height=3.5, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_opacity=0.05)
        rs_label = Text("ReplicaSet (Soll-Zustand: 3)", font_size=20, color=K8S_BLUE, weight=BOLD).next_to(rs_box, UP, buff=0.2).align_to(rs_box, LEFT)
        rs_group = VGroup(rs_box, rs_label).shift(DOWN*0.2)

        # 3 Pods im ReplicaSet
        p1 = create_modern_box("Pod 1", width=2.0, height=1.2, color=NODE_GREEN)
        p2 = create_modern_box("Pod 2", width=2.0, height=1.2, color=NODE_GREEN)
        p3 = create_modern_box("Pod 3", width=2.0, height=1.2, color=NODE_GREEN)
        
        pods = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.6).move_to(rs_box.get_center())

        self.play(DrawBorderThenFill(rs_box), Write(rs_label))
        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(p1[0]), Write(p1[1])),
                AnimationGroup(DrawBorderThenFill(p2[0]), Write(p2[1])),
                AnimationGroup(DrawBorderThenFill(p3[0]), Write(p3[1])),
                lag_ratio=0.2
            )
        )
        self.next_slide()

        # Pod 3 fällt aus
        dead_pod = create_modern_box("Pod 3\n(failed)", width=2.0, height=1.2, color=CTRL_RED).move_to(p3)
        crash_cross = Text("✗", font_size=50, color=CTRL_RED, weight=BOLD).move_to(dead_pod)

        # Sauberer Farbwechsel und Kreuz ohne ablenkendes Wackeln
        self.play(FadeIn(dead_pod), FadeOut(p3))
        self.play(FadeIn(crash_cross, scale=0.5))
        self.wait(0.3)

        # Controller greift ein
        new_pod = create_modern_box("Pod 4\n(Neu)", width=2.0, height=1.2, color=NODE_GREEN).move_to(dead_pod).shift(UP*2.0)
        
        # Dead Pod wird evictiert (fällt nach unten weg), neuer Pod slidet von oben rein
        self.play(
            dead_pod.animate.shift(DOWN*1.5).set_opacity(0),
            crash_cross.animate.shift(DOWN*1.5).set_opacity(0),
            new_pod.animate.move_to(p3),
            run_time=1.2
        )
        self.next_slide()

        # ==========================================
        # SLIDE 3: Failover in Stateful-Clustern
        # ==========================================
        self.play(FadeOut(rs_group), FadeOut(p1), FadeOut(p2), FadeOut(new_pod))
        
        t3 = Text("Failover in Stateful-Clustern (z.B. cnpg)", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        # Hierarchischer Aufbau (Primary oben, Replicas unten)
        primary = create_modern_box("Primary", width=2.5, height=1.2, color=NODE_GREEN).shift(UP*1.0)
        rep1 = create_modern_box("Replica 1\n(Standby)", width=2.5, height=1.2, color=STORE_YELLOW).shift(DOWN*1.2 + LEFT*2.2)
        rep2 = create_modern_box("Replica 2\n(Standby)", width=2.5, height=1.2, color=STORE_YELLOW).shift(DOWN*1.2 + RIGHT*2.2)

        conn1 = create_uniform_arrow(primary.get_bottom(), rep1.get_top(), color=TEXT_MUTED)
        conn2 = create_uniform_arrow(primary.get_bottom(), rep2.get_top(), color=TEXT_MUTED)

        self.play(DrawBorderThenFill(primary[0]), Write(primary[1]))
        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(rep1[0]), Write(rep1[1]), GrowArrow(conn1)),
                AnimationGroup(DrawBorderThenFill(rep2[0]), Write(rep2[1]), GrowArrow(conn2)),
                lag_ratio=0.3
            )
        )
        self.next_slide()

        # Primary stirbt
        dead_primary = create_modern_box("Primary\n(failed)", width=2.5, height=1.2, color=CTRL_RED).move_to(primary)
        cross = Text("✗", font_size=50, color=CTRL_RED, weight=BOLD).move_to(primary)
        
        self.play(FadeIn(dead_primary), FadeOut(primary))
        self.play(FadeIn(cross, scale=0.5))
        self.wait(0.3)

        # Promotion von Replica 1
        promote_box = create_modern_box("Neuer Primary", width=2.5, height=1.2, color=NODE_GREEN).move_to(rep1)
        promote_label = Text("Promotion", font_size=16, color=NODE_GREEN, weight=BOLD).next_to(promote_box, DOWN, buff=0.15)

        self.play(FadeIn(promote_box), FadeOut(rep1), FadeIn(promote_label, shift=UP*0.1))
        
        # Neue Replikations-Verbindung
        new_conn = create_uniform_arrow(promote_box.get_right(), rep2.get_left(), color=TEXT_MUTED)
        
        self.play(
            FadeOut(conn1), FadeOut(conn2), 
            FadeOut(dead_primary), FadeOut(cross),
            GrowArrow(new_conn)
        )
        self.next_slide()

        # ==========================================
        # SLIDE 4: HA auf Infrastrukturebene (3 AZs)
        # ==========================================
        self.play(FadeOut(promote_box), FadeOut(promote_label), FadeOut(rep2), FadeOut(new_conn))
        
        t4 = Text("HA auf Infrastrukturebene", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4))

        # 3 Availability Zones: CP + Workers distributed across AZ A, B, C
        az_positions = [(-3.8, "AZ A"), (0, "AZ B"), (3.8, "AZ C")]
        az_groups = VGroup()
        az_boxes = []

        for x_pos, az_name in az_positions:
            az_box = RoundedRectangle(width=3.0, height=4.0, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_opacity=0.05)
            az_box.shift(RIGHT * x_pos + DOWN * 0.6)
            az_label = Text(az_name, font_size=18, color=NODE_GREEN, weight=BOLD).next_to(az_box, UP, buff=0.2).align_to(az_box, LEFT)

            cp_node = create_modern_box("CP Node", width=2.4, height=0.7, color=K8S_BLUE, font_size=14).move_to(az_box.get_center() + UP * 1.1)
            w1 = create_modern_box("Worker 1", width=2.4, height=0.7, color=NODE_GREEN, font_size=14).move_to(az_box.get_center() + DOWN * 0.6)
            w2 = create_modern_box("Worker 2", width=2.4, height=0.7, color=NODE_GREEN, font_size=14).move_to(az_box.get_center() + DOWN * 1.5)

            az_group = VGroup(az_box, az_label, cp_node, w1, w2)
            az_groups.add(az_group)
            az_boxes.append(az_box)

        self.play(FadeIn(az_groups, shift=UP*0.2))

        # Traffic from top center to all 3 AZs
        traffic = create_modern_box("User Traffic", width=2.4, height=0.7, color=STORE_YELLOW).shift(UP * 2.6)
        self.play(DrawBorderThenFill(traffic[0]), Write(traffic[1]))

        arrows = VGroup()
        for az_box in az_boxes:
            arrow = create_uniform_arrow(traffic.get_bottom(), az_box.get_top(), color=TEXT_LIGHT)
            arrows.add(arrow)
        self.play(*[GrowArrow(a) for a in arrows])
        self.next_slide()

        # AZ B (middle) fails
        az_b_box = az_boxes[1]
        fail_frame = RoundedRectangle(width=3.0, height=4.0, corner_radius=0.2, color=CTRL_RED, stroke_width=4)
        fail_frame.move_to(az_b_box)

        self.play(az_groups[1].animate.set_opacity(0.2), FadeOut(arrows[1]))

        # Traffic redirect to AZ A and AZ C
        self.play(
            arrows[0].animate.set_color(STORE_YELLOW).set_stroke(width=6),
            arrows[2].animate.set_color(STORE_YELLOW).set_stroke(width=6),
        )
        self.next_slide()

        # ==========================================
        # SLIDE 5: Fazit
        # ==========================================
        outro = Text("Kubernetes = Native Redundanz auf jeder Ebene", font_size=BODY_SIZE + 4, color=NODE_GREEN, weight=BOLD)
        self.play(
            *[FadeOut(m) for m in self.mobjects if m != title],
            run_time=1.0
        )
        self.play(Transform(title, outro))
        self.play(title.animate.center().scale(1.1))
        self.next_slide()
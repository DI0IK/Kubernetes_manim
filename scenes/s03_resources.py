from manim import *
from manim_slides import Slide
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY
)
from helpers import create_modern_box


class StandardResources(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("Standard Resources & CRDs", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Deklaratives Paradigma, Resources, Custom Resources", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        self.play(FadeIn(title, shift=UP*0.2), FadeIn(subtitle, shift=UP*0.2))
        self.next_slide()
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Deklaratives Paradigma
        # ==========================================
        t2 = Text("Deklaratives Paradigma", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        # Objekte definieren (Modern Box)
        yaml_box = create_modern_box("YAML\n(Soll-Zustand)", width=2.5, height=1.5, color=NODE_GREEN)
        arrow1 = Arrow(start=LEFT, end=RIGHT, color=TEXT_MUTED, buff=0.2)
        ctrl = create_modern_box("kube-\ncontroller", width=2.5, height=1.5, color=K8S_BLUE)
        arrow2 = Arrow(start=LEFT, end=RIGHT, color=TEXT_MUTED, buff=0.2)
        cluster = create_modern_box("Cluster\n(Ist-Zustand)", width=2.5, height=1.5, color=BOX_GRAY)

        # Sauber als Kette arrangieren
        flow_group = VGroup(yaml_box, arrow1, ctrl, arrow2, cluster).arrange(RIGHT, buff=0.4).move_to(ORIGIN + DOWN*0.2)

        # Klare, schrittweise Animation des Datenflusses ohne unnötige Effekte
        self.play(FadeIn(yaml_box, shift=RIGHT*0.2))
        self.play(GrowArrow(arrow1))
        self.play(FadeIn(ctrl, shift=RIGHT*0.2))
        self.play(GrowArrow(arrow2))
        self.play(FadeIn(cluster, shift=RIGHT*0.2))
        self.next_slide()
        self.play(FadeOut(flow_group))
        
        # ==========================================
        # SLIDE 3: Standard Resource: Pod (Visual + Code)
        # ==========================================
        t3 = Text("Standard Resource: Pod", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        # VISUAL (Left)
        boundary = RoundedRectangle(width=3.6, height=2.8, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_color=NODE_GREEN, fill_opacity=0.05)
        pod_label = Text("Pod", font_size=20, color=NODE_GREEN, weight=BOLD).next_to(boundary, UP, buff=0.2).align_to(boundary, LEFT)
        
        c1_group = create_modern_box("Container A", width=2.8, height=0.8, color=K8S_BLUE, font_size=16)
        c2_group = create_modern_box("Container B", width=2.8, height=0.8, color=STORE_YELLOW, font_size=16)

        containers = VGroup(c1_group, c2_group).arrange(DOWN, buff=0.2).move_to(boundary.get_center())
        ip_label = Text("IP: 10.0.0.1", font_size=14, color=TEXT_MUTED, weight=BOLD).next_to(boundary, DOWN, buff=0.2)
        
        pod_visual = VGroup(boundary, pod_label, containers, ip_label).shift(LEFT * 3 + DOWN*0.2)

        # CODE (Right)
        pod_code = Code(code_file="kubernetes/pod.yaml", language="yaml", background="window").scale(0.75).shift(RIGHT * 3 + DOWN*0.2)

        # Purposeful animation: Boundary -> Contents -> IP -> Code
        self.play(FadeIn(boundary), Write(pod_label))
        self.play(FadeIn(c1_group, shift=UP*0.1), FadeIn(c2_group, shift=UP*0.1))
        self.play(FadeIn(ip_label))
        self.play(FadeIn(pod_code, shift=LEFT*0.2))
        self.next_slide()

        self.play(FadeOut(pod_visual), FadeOut(pod_code))
        
        # ==========================================
        # SLIDE 4: Standard Resource: Deployment (Visual + Code)
        # ==========================================
        t4 = Text("Standard Resource: Deployment", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4))

        # VISUAL (Left)
        dep_boundary = RoundedRectangle(width=3.6, height=3.2, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_color=K8S_BLUE, fill_opacity=0.05)
        dep_label = Text("Deployment (replicas: 3)", font_size=20, color=K8S_BLUE, weight=BOLD).next_to(dep_boundary, UP, buff=0.2).align_to(dep_boundary, LEFT)
        
        dp1 = create_modern_box("Pod 1", width=2.8, height=0.6, color=NODE_GREEN, font_size=16)
        dp2 = create_modern_box("Pod 2", width=2.8, height=0.6, color=NODE_GREEN, font_size=16)
        dp3 = create_modern_box("Pod 3", width=2.8, height=0.6, color=NODE_GREEN, font_size=16)

        dep_pods = VGroup(dp1, dp2, dp3).arrange(DOWN, buff=0.2).move_to(dep_boundary.get_center())
        dep_visual = VGroup(dep_boundary, dep_label, dep_pods).shift(LEFT * 3 + DOWN*0.2)

        # CODE (Right)
        dep_code = Code(code_file="kubernetes/deployment-simple.yaml", language="yaml", background="window").scale(0.75).shift(RIGHT * 3 + DOWN*0.2)

        # Purposeful animation
        self.play(FadeIn(dep_boundary), Write(dep_label))
        self.play(FadeIn(dp1, shift=UP*0.1), FadeIn(dp2, shift=UP*0.1), FadeIn(dp3, shift=UP*0.1))
        self.play(FadeIn(dep_code, shift=LEFT*0.2))
        self.next_slide()

        self.play(FadeOut(dep_visual), FadeOut(dep_code))

        # ==========================================
        # SLIDE 5: Standard Resource: Service (Visual + Code)
        # ==========================================
        t5 = Text("Standard Resource: Service", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t5))

        # VISUAL (Left)
        svc_box = create_modern_box("Service\n(Traffic Router)", width=2.5, height=1.2, color=STORE_YELLOW, font_size=18).move_to(LEFT * 4.5 + DOWN*0.2)
        
        sp1 = create_modern_box("Pod 1", width=2.0, height=0.6, color=NODE_GREEN, font_size=14)
        sp2 = create_modern_box("Pod 2", width=2.0, height=0.6, color=NODE_GREEN, font_size=14)
        sp3 = create_modern_box("Pod 3", width=2.0, height=0.6, color=NODE_GREEN, font_size=14)
        svc_pods = VGroup(sp1, sp2, sp3).arrange(DOWN, buff=0.2).move_to(LEFT * 1.5 + DOWN*0.2)

        a1 = Arrow(svc_box.get_right(), sp1.get_left(), color=TEXT_MUTED, buff=0.1)
        a2 = Arrow(svc_box.get_right(), sp2.get_left(), color=TEXT_MUTED, buff=0.1)
        a3 = Arrow(svc_box.get_right(), sp3.get_left(), color=TEXT_MUTED, buff=0.1)
        
        user_arrow = Arrow(svc_box.get_left() + LEFT*1.5, svc_box.get_left(), color=TEXT_LIGHT, buff=0.1)
        user_label = Text("Traffic", font_size=16, color=TEXT_LIGHT).next_to(user_arrow, UP, buff=0.1)

        svc_visual = VGroup(svc_box, svc_pods, a1, a2, a3, user_arrow, user_label)

        # CODE (Right)
        svc_code = Code(code_file="kubernetes/service-simple.yaml", language="yaml", background="window").scale(0.75).shift(RIGHT * 3 + DOWN*0.2)

        # Purposeful animation
        self.play(FadeIn(svc_box, shift=UP*0.2))
        self.play(FadeIn(svc_pods, shift=UP*0.2))
        self.play(
            GrowArrow(user_arrow), FadeIn(user_label),
            GrowArrow(a1), GrowArrow(a2), GrowArrow(a3)
        )
        self.play(FadeIn(svc_code, shift=LEFT*0.2))
        self.next_slide()

        self.play(FadeOut(svc_visual), FadeOut(svc_code))

        # ==========================================
        # SLIDE 6: CRDs
        # ==========================================
        t6 = Text("Custom Resource Definitions (CRDs)", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t6))

        # Alle Puzzleteile definieren und in eine Reihe packen
        k8s_api = Circle(radius=0.9, color=K8S_BLUE, stroke_width=2, fill_color=K8S_BLUE, fill_opacity=BG_BOX_OPACITY)
        k8s_label = Text("K8s API", font_size=18, color=TEXT_LIGHT, weight=BOLD).move_to(k8s_api)
        k8s_group = VGroup(k8s_api, k8s_label)

        plus1 = Text("+", font_size=36, color=TEXT_MUTED)
        crd_piece = create_modern_box("CRD", width=1.5, height=1.0, color=STORE_YELLOW)
        plus2 = Text("+", font_size=36, color=TEXT_MUTED)

        op_circle = Circle(radius=0.7, color=NODE_GREEN, stroke_width=2, fill_color=NODE_GREEN, fill_opacity=BG_BOX_OPACITY)
        op_label = Text("Operator", font_size=16, color=TEXT_LIGHT, weight=BOLD).move_to(op_circle)
        op_group = VGroup(op_circle, op_label)

        eq = Text("=", font_size=36, color=TEXT_MUTED)
        ext = create_modern_box("Erweiterte\nAPI", width=2.2, height=1.2, color=CTRL_RED)

        puzzle_group = VGroup(k8s_group, plus1, crd_piece, plus2, op_group, eq, ext).arrange(RIGHT, buff=0.35).move_to(ORIGIN)

        # Lineare Gleichung aufbauen ohne ablenkende Rotation/Skalierung
        self.play(FadeIn(k8s_group, shift=RIGHT*0.2))
        self.play(Write(plus1), FadeIn(crd_piece, shift=RIGHT*0.2))
        self.play(Write(plus2), FadeIn(op_group, shift=RIGHT*0.2))
        self.play(Write(eq), FadeIn(ext, shift=RIGHT*0.2))
        self.next_slide()

        self.play(FadeOut(puzzle_group))
        
        # ==========================================
        # SLIDE 7: CRD Beispiel
        # ==========================================
        t7 = Text("Beispiel: CloudNativePG", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t7))

        cnpg_code = Code(code_file="kubernetes/cnpg-cluster-simple.yaml", language="yaml", background="window").scale(0.75)
        self.play(FadeIn(cnpg_code, shift=UP*0.2))
            
        self.next_slide()

        # ==========================================
        # SLIDE 8: Fazit
        # ==========================================
        outro = Text("CRDs machen Kubernetes grenzenlos erweiterbar", font_size=BODY_SIZE + 2, color=NODE_GREEN, weight=BOLD)
        
        fade_out_group = VGroup(cnpg_code)
        if 'highlight_rect' in locals():
            fade_out_group.add(highlight_rect)
            
        self.play(FadeOut(fade_out_group), Transform(title, outro))
        self.play(title.animate.center().scale(1.1))
        self.next_slide()
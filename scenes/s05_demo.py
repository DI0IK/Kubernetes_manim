from manim import *
from manim_slides import Slide
from style import (
    TEXT_INVERTED, TITLE_SIZE, BODY_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, TEXT_INVERTED_MUTED, BG_BOX_OPACITY,
    GIT_ORANGE, TERMINAL_BG, TERMINAL_BAR
)
from helpers import create_modern_box, create_uniform_arrow


class DemoDeployment(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("Demo: Full-Stack GitOps", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Datenbank → Backend → LoadBalancer", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        self.play(FadeIn(title, shift=UP*0.2), FadeIn(subtitle, shift=UP*0.2))
        self.next_slide()
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Split-Screen Setup (Architektur & Terminal)
        # ==========================================
        
        # --- LEFT: Visual Architecture ---
        # 3 Columns Layout: DB (Left), Web (Center), LB (Right)
        git_box = create_modern_box("Git Repo", width=2.0, height=1.0, color=GIT_ORANGE, font_size=16).move_to(LEFT * 5.2 + UP * 1.6)
        argo_box = create_modern_box("ArgoCD", width=2.0, height=1.0, color=STORE_YELLOW, font_size=16).move_to(LEFT * 2.6 + UP * 1.6)
        
        op_box = create_modern_box("cnpg Operator", width=2.0, height=1.0, color=CTRL_RED, font_size=14).move_to(LEFT * 5.2 + DOWN * 0.2)
        api_box = create_modern_box("K8s API", width=2.0, height=1.0, color=K8S_BLUE, font_size=16).move_to(LEFT * 2.6 + DOWN * 0.2)
        
        # Infrastructure Boundaries (Empty initially)
        pg_boundary = RoundedRectangle(width=2.0, height=2.4, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_opacity=0.05).move_to(LEFT * 5.2 + DOWN * 2.4)
        pg_label = Text("PostgreSQL", font_size=14, color=NODE_GREEN, weight=BOLD).next_to(pg_boundary.get_top(), DOWN, buff=0.1)
        
        web_boundary = RoundedRectangle(width=1.8, height=2.4, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_opacity=0.05).move_to(LEFT * 2.6 + DOWN * 2.4)
        web_label = Text("Web App", font_size=14, color=K8S_BLUE, weight=BOLD).next_to(web_boundary.get_top(), DOWN, buff=0.1)
        
        lb_box = create_modern_box("Load\nBalancer", width=1.2, height=2.4, color=STORE_YELLOW, font_size=14).move_to(LEFT * 0.6 + DOWN * 2.4)

        visual_group = VGroup(git_box, argo_box, op_box, api_box, pg_boundary, pg_label, web_boundary, web_label, lb_box)

        # --- RIGHT: Modern Terminal ---
        term_w, term_h = 6.2, 6.2  # Narrowed slightly to fit 3-col layout
        term_frame = RoundedRectangle(width=term_w, height=term_h, corner_radius=0.15, color=TERMINAL_BAR, fill_color=TERMINAL_BG, fill_opacity=1.0).move_to(RIGHT * 3.5 + DOWN * 0.4)
        
        term_bar = RoundedRectangle(width=term_w, height=0.4, corner_radius=0.15, color=TERMINAL_BAR, fill_color=TERMINAL_BAR, fill_opacity=1.0).align_to(term_frame, UP).align_to(term_frame, LEFT)
        term_bar_bottom = Rectangle(width=term_w, height=0.2, color=TERMINAL_BAR, fill_color=TERMINAL_BAR, fill_opacity=1.0).align_to(term_bar, DOWN).align_to(term_bar, LEFT)
        
        dot_r = Circle(radius=0.06, color="#FF5F56", fill_color="#FF5F56", fill_opacity=1)
        dot_y = Circle(radius=0.06, color="#FFBD2E", fill_color="#FFBD2E", fill_opacity=1)
        dot_g = Circle(radius=0.06, color="#27C93F", fill_color="#27C93F", fill_opacity=1)
        dots = VGroup(dot_r, dot_y, dot_g).arrange(RIGHT, buff=0.1).move_to(term_bar.get_center()).align_to(term_bar, LEFT).shift(RIGHT * 0.2)
        term_title_text = Text("deploy-demo ~ zsh", font_size=13, color=TEXT_INVERTED_MUTED).move_to(term_bar.get_center())
        
        terminal_ui = VGroup(term_frame, term_bar, term_bar_bottom, dots, term_title_text)

        self.play(FadeIn(visual_group, shift=RIGHT*0.2))
        self.play(DrawBorderThenFill(term_frame), FadeIn(VGroup(term_bar, term_bar_bottom, dots, term_title_text)))
        self.next_slide()

        # ==========================================
        # PHASE 1: Deploy PostgreSQL
        # ==========================================
        
        # 1. Show YAML
        pg_code = Code(code_file="kubernetes/cnpg-cluster-simple.yaml", language="yaml", background="window").scale(0.8).center()
        try: pg_code[0][0].set_fill(opacity=0.95)
        except: pass

        self.play(FadeIn(pg_code, shift=UP*0.2))
        self.next_slide()

        # Commit to Git
        self.play(pg_code.animate.scale(0.1).move_to(git_box.get_center()).set_opacity(0), run_time=0.8)

        # Terminal Variables
        t_start = term_frame.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.6
        t_font = 12 

        # Git Push -> Argo -> API -> Op
        l1 = Text("$ git push origin main", font_size=t_font, color=STORE_YELLOW, font="Monospace").move_to(t_start, aligned_edge=UL)
        self.play(AddTextLetterByLetter(l1, run_time=0.6))
        
        arrow_git_argo = create_uniform_arrow(git_box.get_right(), argo_box.get_left())
        self.play(GrowArrow(arrow_git_argo))
        
        l2 = Text("remote: [ArgoCD] Syncing 'pg-cluster'...", font_size=t_font, color=K8S_BLUE, font="Monospace").next_to(l1, DOWN, buff=0.15).align_to(l1, LEFT)
        self.play(Write(l2, run_time=0.4))
        
        arrow_argo_api = create_uniform_arrow(argo_box.get_bottom(), api_box.get_top())
        self.play(GrowArrow(arrow_argo_api))

        l3 = Text("=> [cnpg] Reconciling Cluster...", font_size=t_font, color=CTRL_RED, font="Monospace").next_to(l2, DOWN, buff=0.15).align_to(l1, LEFT)
        self.play(Write(l3, run_time=0.5))

        arrow_api_op = create_uniform_arrow(api_box.get_left(), op_box.get_right())
        self.play(GrowArrow(arrow_api_op))
        self.next_slide()

        # Pods Pending -> Running
        l4 = Text("$ kubectl get pods -n database -w", font_size=t_font, color=STORE_YELLOW, font="Monospace").next_to(l3, DOWN, buff=0.3).align_to(l1, LEFT)
        self.play(AddTextLetterByLetter(l4, run_time=0.6))

        arrow_op_pg = create_uniform_arrow(op_box.get_bottom(), pg_boundary.get_top())
        self.play(GrowArrow(arrow_op_pg))

        l5 = Text("NAME           READY  STATUS", font_size=t_font, color=TEXT_INVERTED, font="Monospace").next_to(l4, DOWN, buff=0.1).align_to(l1, LEFT)
        l6_pend = Text("pg-0           0/1    Pending", font_size=t_font, color=TEXT_INVERTED_MUTED, font="Monospace").next_to(l5, DOWN, buff=0.1).align_to(l1, LEFT)
        l7_pend = Text("pg-1           0/1    Pending", font_size=t_font, color=TEXT_INVERTED_MUTED, font="Monospace").next_to(l6_pend, DOWN, buff=0.1).align_to(l1, LEFT)
        l8_pend = Text("pg-2           0/1    Pending", font_size=t_font, color=TEXT_INVERTED_MUTED, font="Monospace").next_to(l7_pend, DOWN, buff=0.1).align_to(l1, LEFT)

        p1 = create_modern_box("pg-0", width=1.6, height=0.4, color=NODE_GREEN, font_size=12)
        p2 = create_modern_box("pg-1", width=1.6, height=0.4, color=NODE_GREEN, font_size=12)
        p3 = create_modern_box("pg-2", width=1.6, height=0.4, color=NODE_GREEN, font_size=12)
        for p in [p1, p2, p3]: p[0].set_fill(opacity=0)
        pg_pods = VGroup(p1, p2, p3).arrange(DOWN, buff=0.15).next_to(pg_label, DOWN, buff=0.15)

        self.play(FadeIn(l5), FadeIn(l6_pend), FadeIn(l7_pend), FadeIn(l8_pend))
        self.play(Create(p1[0]), Write(p1[1]), Create(p2[0]), Write(p2[1]), Create(p3[0]), Write(p3[1]))
        self.next_slide()

        l6_run = Text("pg-0           1/1    Running", font_size=t_font, color=NODE_GREEN, font="Monospace").move_to(l6_pend, aligned_edge=LEFT)
        l7_run = Text("pg-1           1/1    Running", font_size=t_font, color=NODE_GREEN, font="Monospace").move_to(l7_pend, aligned_edge=LEFT)
        l8_run = Text("pg-2           1/1    Running", font_size=t_font, color=NODE_GREEN, font="Monospace").move_to(l8_pend, aligned_edge=LEFT)

        self.play(
            Transform(l6_pend, l6_run), Transform(l7_pend, l7_run), Transform(l8_pend, l8_run),
            p1[0].animate.set_fill(opacity=BG_BOX_OPACITY), p2[0].animate.set_fill(opacity=BG_BOX_OPACITY), p3[0].animate.set_fill(opacity=BG_BOX_OPACITY)
        )
        self.next_slide()

        # ==========================================
        # PHASE 2: Deploy Web App & LoadBalancer
        # ==========================================
        
        # Clear Terminal
        term_content_p1 = VGroup(l1, l2, l3, l4, l5, l6_pend, l7_pend, l8_pend)
        self.play(FadeOut(term_content_p1))
        
        # Show Web YAMLs (one at a time)
        web_deploy_code = Code(code_file="kubernetes/web-deploy.yaml", language="yaml", background="window").scale(0.8).center()
        try: web_deploy_code[0][0].set_fill(opacity=0.95)
        except: pass
        web_svc_code = Code(code_file="kubernetes/web-svc.yaml", language="yaml", background="window").scale(0.8).center()
        try: web_svc_code[0][0].set_fill(opacity=0.95)
        except: pass

        self.play(FadeIn(web_deploy_code, shift=UP*0.2))
        self.next_slide()

        self.play(FadeOut(web_deploy_code), FadeIn(web_svc_code, shift=UP*0.2))
        self.next_slide()

        # Commit both to Git
        self.play(FadeOut(web_svc_code), run_time=0.8)

        # Git Push -> Argo -> API
        t1 = Text("$ git push origin main", font_size=t_font, color=STORE_YELLOW, font="Monospace").move_to(t_start, aligned_edge=UL)
        self.play(AddTextLetterByLetter(t1, run_time=0.6))
        
        self.play(Indicate(arrow_git_argo, color=STORE_YELLOW))
        
        t2 = Text("remote: [ArgoCD] Syncing 'web-app'...", font_size=t_font, color=K8S_BLUE, font="Monospace").next_to(t1, DOWN, buff=0.15).align_to(t1, LEFT)
        self.play(Write(t2, run_time=0.4))
        
        self.play(Indicate(arrow_argo_api, color=STORE_YELLOW))

        # API deploys Web Pods & LB
        t3 = Text("$ kubectl get pods -n web -w", font_size=t_font, color=STORE_YELLOW, font="Monospace").next_to(t2, DOWN, buff=0.3).align_to(t1, LEFT)
        self.play(AddTextLetterByLetter(t3, run_time=0.6))

        arrow_api_web = create_uniform_arrow(api_box.get_bottom(), web_boundary.get_top())
        arrow_api_lb = create_uniform_arrow(api_box.get_bottom(), lb_box.get_top())
        self.play(GrowArrow(arrow_api_web), GrowArrow(arrow_api_lb))

        t4 = Text("NAME           READY  STATUS", font_size=t_font, color=TEXT_INVERTED, font="Monospace").next_to(t3, DOWN, buff=0.1).align_to(t1, LEFT)
        t5_pend = Text("web-0          0/1    Pending", font_size=t_font, color=TEXT_INVERTED_MUTED, font="Monospace").next_to(t4, DOWN, buff=0.1).align_to(t1, LEFT)
        t6_pend = Text("web-1          0/1    Pending", font_size=t_font, color=TEXT_INVERTED_MUTED, font="Monospace").next_to(t5_pend, DOWN, buff=0.1).align_to(t1, LEFT)

        w1 = create_modern_box("web-0", width=1.4, height=0.4, color=K8S_BLUE, font_size=12)
        w2 = create_modern_box("web-1", width=1.4, height=0.4, color=K8S_BLUE, font_size=12)
        for w in [w1, w2]: w[0].set_fill(opacity=0)
        web_pods = VGroup(w1, w2).arrange(DOWN, buff=0.15).next_to(web_label, DOWN, buff=0.15)

        self.play(FadeIn(t4), FadeIn(t5_pend), FadeIn(t6_pend))
        self.play(Create(w1[0]), Write(w1[1]), Create(w2[0]), Write(w2[1]))
        self.next_slide()

        t5_run = Text("web-0          1/1    Running", font_size=t_font, color=NODE_GREEN, font="Monospace").move_to(t5_pend, aligned_edge=LEFT)
        t6_run = Text("web-1          1/1    Running", font_size=t_font, color=NODE_GREEN, font="Monospace").move_to(t6_pend, aligned_edge=LEFT)

        self.play(
            Transform(t5_pend, t5_run), Transform(t6_pend, t6_run),
            w1[0].animate.set_fill(opacity=BG_BOX_OPACITY), w2[0].animate.set_fill(opacity=BG_BOX_OPACITY)
        )
        self.next_slide()

        # Database Connection Arrow
        conn_arrow = create_uniform_arrow(web_boundary.get_left(), pg_boundary.get_right(), color=STORE_YELLOW)
        conn_label = Text("DB Auth", font_size=12, color=STORE_YELLOW, weight=BOLD).next_to(conn_arrow, UP, buff=0.05)
        self.play(GrowArrow(conn_arrow), FadeIn(conn_label))
        self.next_slide()

        # LoadBalancer IP Assignment
        t7 = Text("$ kubectl get svc -n web web-lb -w", font_size=t_font, color=STORE_YELLOW, font="Monospace").next_to(t6_pend, DOWN, buff=0.3).align_to(t1, LEFT)
        self.play(AddTextLetterByLetter(t7, run_time=0.6))
        
        t8 = Text("NAME      TYPE           EXTERNAL-IP   PORT(S)", font_size=t_font, color=TEXT_INVERTED, font="Monospace").next_to(t7, DOWN, buff=0.1).align_to(t1, LEFT)
        t9_pend = Text("web-lb    LoadBalancer   <pending>     80:31200/TCP", font_size=t_font, color=TEXT_INVERTED_MUTED, font="Monospace").next_to(t8, DOWN, buff=0.1).align_to(t1, LEFT)
        
        self.play(FadeIn(t8), FadeIn(t9_pend))
        self.next_slide()

        t9_run = Text("web-lb    LoadBalancer   203.0.113.50  80:31200/TCP", font_size=t_font, color=NODE_GREEN, font="Monospace").move_to(t9_pend, aligned_edge=LEFT)
        lb_traffic_arrow = create_uniform_arrow(lb_box.get_left(), web_boundary.get_right(), color=TEXT_LIGHT)
        lb_label = Text("Port 80", font_size=12, color=TEXT_LIGHT, weight=BOLD).next_to(lb_traffic_arrow, UP, buff=0.05)

        self.play(Transform(t9_pend, t9_run))
        self.play(GrowArrow(lb_traffic_arrow), FadeIn(lb_label))
        self.next_slide()

        # ==========================================
        # SLIDE 10: Fazit
        # ==========================================
        outro = Text("Full-Stack Projekt erfolgreich deployed via GitOps", font_size=BODY_SIZE + 2, color=NODE_GREEN, weight=BOLD)
        
        # Cleanup everything except the title
        self.play(
            *[FadeOut(m) for m in self.mobjects if m != title],
            run_time=1.0
        )
        self.play(Transform(title, outro))
        self.play(title.animate.center().scale(1.1))
        self.next_slide()
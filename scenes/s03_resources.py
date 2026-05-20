from manim import *
from manim_slides import Slide
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY
)
from helpers import create_modern_box, create_uniform_arrow


class StandardResources(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("Standard Resources & CRDs", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Deklaratives Paradigma, Resources, Custom Resources", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        self.play(FadeIn(title, shift=UP*0.2), FadeIn(subtitle, shift=UP*0.2))
        self.next_slide(notes="**Deklaratives Paradigma** – Benutzer definiert Soll-Zustand in YAML. Controller (z.B. Deployment-Controller) gleichen Ist-Zustand an. Keine imperativen Schritte nötig.")
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Deklaratives Paradigma
        # ==========================================
        t2 = Text("Deklaratives Paradigma", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        # Objekte definieren (Modern Box)
        yaml_box = create_modern_box("YAML\n(Soll-Zustand)", width=2.5, height=1.5, color=NODE_GREEN)
        arrow1 = create_uniform_arrow(LEFT, RIGHT)
        ctrl = create_modern_box("kube-\ncontroller", width=2.5, height=1.5, color=K8S_BLUE)
        arrow2 = create_uniform_arrow(LEFT, RIGHT)
        cluster = create_modern_box("Cluster\n(Ist-Zustand)", width=2.5, height=1.5, color=BOX_GRAY)

        # Sauber als Kette arrangieren
        flow_group = VGroup(yaml_box, arrow1, ctrl, arrow2, cluster).arrange(RIGHT, buff=0.4).move_to(ORIGIN + DOWN*0.2)

        # Klare, schrittweise Animation des Datenflusses ohne unnötige Effekte
        self.play(FadeIn(yaml_box, shift=RIGHT*0.2))
        self.play(GrowArrow(arrow1))
        self.play(FadeIn(ctrl, shift=RIGHT*0.2))
        self.play(GrowArrow(arrow2))
        self.play(FadeIn(cluster, shift=RIGHT*0.2))
        self.next_slide(notes="**Namespaces** – virtuelle Cluster innerhalb eines physischen Clusters. Bieten Isolation und Organisation. Ressourcen innerhalb eines Namespace sind per DNS erreichbar: `service.namespace.svc.cluster.local`.")
        self.play(FadeOut(flow_group))

        # ==========================================
        # SLIDE 3: Namespaces
        # ==========================================
        t_ns = Text("Namespaces", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t_ns))

        ns_default = RoundedRectangle(width=3.0, height=3.0, corner_radius=0.2, color=BOX_GRAY, stroke_width=2, fill_opacity=0.05).shift(LEFT * 3.8 + DOWN * 0.4)
        ns_db = RoundedRectangle(width=3.0, height=3.0, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_opacity=0.05).shift(DOWN * 0.4)
        ns_web = RoundedRectangle(width=3.0, height=3.0, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_opacity=0.05).shift(RIGHT * 3.8 + DOWN * 0.4)

        l_default = Text("default", font_size=20, color=BOX_GRAY, weight=BOLD).next_to(ns_default, UP, buff=0.2).align_to(ns_default, LEFT)
        l_db = Text("database", font_size=20, color=K8S_BLUE, weight=BOLD).next_to(ns_db, UP, buff=0.2).align_to(ns_db, LEFT)
        l_web = Text("web", font_size=20, color=NODE_GREEN, weight=BOLD).next_to(ns_web, UP, buff=0.2).align_to(ns_web, LEFT)

        r_default = VGroup(
            create_modern_box("Pod: my-pod", width=2.4, height=0.6, color=NODE_GREEN, font_size=13),
            create_modern_box("Svc: my-app-svc", width=2.4, height=0.6, color=STORE_YELLOW, font_size=13),
        ).arrange(DOWN, buff=0.2).move_to(ns_default.get_center())

        r_db = VGroup(
            create_modern_box("Cluster: pg-cluster", width=2.4, height=0.6, color=CTRL_RED, font_size=13),
        ).move_to(ns_db.get_center())

        r_web = VGroup(
            create_modern_box("Deploy: web-app", width=2.4, height=0.6, color=NODE_GREEN, font_size=13),
            create_modern_box("Svc: web-lb", width=2.4, height=0.6, color=STORE_YELLOW, font_size=13),
        ).arrange(DOWN, buff=0.2).move_to(ns_web.get_center())

        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(ns_default), Write(l_default), FadeIn(r_default, shift=UP*0.2)),
                AnimationGroup(DrawBorderThenFill(ns_db), Write(l_db), FadeIn(r_db, shift=UP*0.2)),
                AnimationGroup(DrawBorderThenFill(ns_web), Write(l_web), FadeIn(r_web, shift=UP*0.2)),
                lag_ratio=0.25
            )
        )

        ns_note = Text("Virtuelle Cluster zur Isolation & Organisation", font_size=18, color=TEXT_MUTED).next_to(ns_db, DOWN, buff=0.4)
        self.play(FadeIn(ns_note, shift=UP*0.2))
        self.next_slide(notes="**Pod** – kleinste Einheit, ein oder mehrere Container. Teilen sich Network-Namespace (gleiche IP) und Storage. Meist 1 Container pro Pod (Sidecar-Container sind möglich).")

        self.play(FadeOut(ns_default), FadeOut(ns_db), FadeOut(ns_web),
                  FadeOut(l_default), FadeOut(l_db), FadeOut(l_web),
                  FadeOut(r_default), FadeOut(r_db), FadeOut(r_web),
                  FadeOut(ns_note))

        # ==========================================
        # SLIDE 4: Standard Resource: Pod (Visual + Code)
        # ==========================================
        t3 = Text("Standard Resource: Pod", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        # VISUAL (Left)
        boundary = RoundedRectangle(width=3.6, height=2.8, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_color=NODE_GREEN, fill_opacity=0.05)
        pod_label = Text("Pod", font_size=20, color=NODE_GREEN, weight=BOLD).next_to(boundary, UP, buff=0.2).align_to(boundary, LEFT)
        
        c1_group = create_modern_box("Container A", width=2.8, height=0.8, color=K8S_BLUE, font_size=16)
        c2_group = create_modern_box("Container B", width=2.8, height=0.8, color=STORE_YELLOW, font_size=16)

        containers = VGroup(c1_group, c2_group).arrange(DOWN, buff=0.2).move_to(boundary.get_center())
        
        pod_visual = VGroup(boundary, pod_label, containers).shift(LEFT * 3 + DOWN*0.2)

        # CODE (Right)
        pod_code = Code(code_file="kubernetes/pod.yaml", language="yaml", background="window").scale(0.75).shift(RIGHT * 3 + DOWN*0.2)

        # Purposeful animation: Boundary -> Contents -> IP -> Code
        self.play(FadeIn(boundary), Write(pod_label))
        self.play(FadeIn(c1_group, shift=UP*0.1), FadeIn(c2_group, shift=UP*0.1))
        self.play(FadeIn(pod_code, shift=LEFT*0.2))
        self.next_slide(notes="**Deployment** – deklariert Soll-Zustand für Pods (replicas). Erzeugt ReplicaSet, das die Pods überwacht. Rolling Updates mit null Ausfallzeit.")

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
        self.next_slide(notes="**Service** – stabiler Endpunkt für eine Gruppe von Pods. Pods sind ephemer (wechselnde IPs), Services bieten eine feste IP und DNS. Typen: ClusterIP, NodePort, LoadBalancer.")

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

        a1 = create_uniform_arrow(svc_box.get_right(), sp1.get_left())
        a2 = create_uniform_arrow(svc_box.get_right(), sp2.get_left())
        a3 = create_uniform_arrow(svc_box.get_right(), sp3.get_left())
        
        user_arrow = create_uniform_arrow(svc_box.get_left() + LEFT*1.5, svc_box.get_left(), color=TEXT_LIGHT)
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
        self.next_slide(notes="**Internal DNS** – CoreDNS ist der Cluster-DNS. Namensauflösung: `servicename.namespace.svc.cluster.local`. Pod → Service → Cluster-IP. Der `cluster.local`-Suffix ist konfigurierbar.")

        self.play(FadeOut(svc_visual), FadeOut(svc_code))

        # ==========================================
        # SLIDE 7: Internal DNS & Service Discovery
        # ==========================================
        t_dns = Text("Internal DNS & Service Discovery", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t_dns))

        dns_name = MarkupText(
            f'<span fgcolor="{NODE_GREEN}" weight="bold">my-svc</span>'
            f'<span fgcolor="{TEXT_MUTED}">.</span>'
            f'<span fgcolor="{K8S_BLUE}" weight="bold">my-ns</span>'
            f'<span fgcolor="{TEXT_MUTED}">.</span>'
            f'<span fgcolor="{STORE_YELLOW}" weight="bold">svc</span>'
            f'<span fgcolor="{TEXT_MUTED}">.cluster.local</span>',
            font_size=26
        ).move_to(UP * 1.8)

        self.play(FadeIn(dns_name, shift=DOWN*0.2))
        self.next_slide(notes="**CoreDNS** – Kubernetes-interner DNS-Server, läuft als Pod im kube-system Namespace. Jeder neue Service erhält automatisch einen DNS-Eintrag.")

        pod_dns = create_modern_box("Pod", width=2.0, height=1.0, color=NODE_GREEN).shift(LEFT * 4.5 + DOWN * 1.0)
        coredns = create_modern_box("CoreDNS", width=2.0, height=1.0, color=K8S_BLUE).shift(DOWN * 1.0)
        svc_dns = create_modern_box("Service\n(my-svc)", width=2.0, height=1.0, color=STORE_YELLOW).shift(RIGHT * 4.5 + DOWN * 1.0)

        arrow1_dns = create_uniform_arrow(pod_dns.get_right(), coredns.get_left())
        arrow2_dns = create_uniform_arrow(coredns.get_right(), svc_dns.get_left())
        label1_dns = Text("DNS Query", font_size=14, color=TEXT_MUTED, weight=BOLD).next_to(arrow1_dns, UP, buff=0.1)
        label2_dns = Text("Cluster IP", font_size=14, color=TEXT_MUTED, weight=BOLD).next_to(arrow2_dns, UP, buff=0.1)

        self.play(FadeIn(pod_dns, shift=RIGHT*0.3), FadeIn(svc_dns, shift=LEFT*0.3))
        self.play(FadeIn(coredns, shift=UP*0.3))
        self.play(GrowArrow(arrow1_dns), FadeIn(label1_dns))
        self.play(GrowArrow(arrow2_dns), FadeIn(label2_dns))
        self.next_slide(notes="**CRDs** (Custom Resource Definitions) – erweitern die K8s-API um benutzerdefinierte Ressourcen. **Operator** – ein Controller, der die CRD-Logik implementiert, z.B. CloudNativePG (PostgreSQL).")

        self.play(FadeOut(dns_name),
                  FadeOut(pod_dns), FadeOut(coredns), FadeOut(svc_dns),
                  FadeOut(arrow1_dns), FadeOut(arrow2_dns),
                  FadeOut(label1_dns), FadeOut(label2_dns))

        # ==========================================
        # SLIDE 8: CRDs
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
        self.next_slide(notes="**CloudNativePG** (cnpg) – PostgreSQL-Operator für K8s. Definiert Datenbank-Cluster als CRD. Übernimmt Backup, Failover, Replikation automatisch.")

        self.play(FadeOut(puzzle_group))
        
        # ==========================================
        # SLIDE 9: CRD Beispiel
        # ==========================================
        t7 = Text("Beispiel: CloudNativePG", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t7))

        cnpg_code = Code(code_file="kubernetes/cnpg-cluster-simple.yaml", language="yaml", background="window").scale(0.75)
        self.play(FadeIn(cnpg_code, shift=UP*0.2))

        self.next_slide(notes="**Weitere Resources** – ConfigMap/Secret (Konfiguration), Ingress (L7-Routing), PVC (persistenter Speicher), DaemonSet (ein Pod pro Node), StatefulSet (stabile Identitäten), NetworkPolicy (Firewall).")

        # ==========================================
        # SLIDE 10: Weitere wichtige Resources
        # ==========================================
        self.play(FadeOut(cnpg_code))
        t_more = Text("Weitere wichtige Resources", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t_more))

        cards_data = [
            ("ConfigMap / Secret", "Konfiguration & Secrets\nentkoppelt vom Pod-Image", STORE_YELLOW),
            ("Ingress", "L7 Routing per Host/Path\nzu internen Services", K8S_BLUE),
            ("PersistentVolumeClaim", "Persistenten Speicher\nper StorageClass anfordern", NODE_GREEN),
            ("DaemonSet", "Ein Pod pro Node\n(Logging, Monitoring, CNI)", BOX_GRAY),
            ("StatefulSet", "Stabile Pod-Namen\n& persistent Storage", CTRL_RED),
            ("NetworkPolicy", "Firewall-Regeln\nzwischen Pods", STORE_YELLOW),
        ]

        cards = VGroup()
        for i, (title_text, desc, color) in enumerate(cards_data):
            x = -3.0 if i % 2 == 0 else 3.0
            y = 2 if i < 2 else (0.0 if i < 4 else -2)
            card = RoundedRectangle(width=5.6, height=1.6, corner_radius=0.2, color=color, stroke_width=2, fill_color=color, fill_opacity=0.04)
            card.shift(RIGHT * x + DOWN * y)
            t_card = Text(title_text, font_size=18, color=TEXT_LIGHT, weight=BOLD).move_to(card.get_center() + UP * 0.3)
            d_card = Text(desc, font_size=13, color=TEXT_MUTED, line_spacing=1.3).move_to(card.get_center() + DOWN * 0.4)
            cards.add(VGroup(card, t_card, d_card))

        self.play(LaggedStart(*[FadeIn(g, shift=UP*0.3) for g in cards], lag_ratio=0.15))
        self.next_slide(notes="**Fazit** – CRDs machen Kubernetes grenzenlos erweiterbar. Fast jede Stateful-Anwendung (DB, Queue, Monitoring) hat inzwischen einen Operator.")

        self.play(FadeOut(cards))

        # ==========================================
        # SLIDE 11: Fazit
        # ==========================================
        outro = Text("CRDs machen Kubernetes grenzenlos erweiterbar", font_size=BODY_SIZE + 2, color=NODE_GREEN, weight=BOLD)
        
        self.play(Transform(title, outro))
        self.play(title.animate.center().scale(1.1))
        self.next_slide()

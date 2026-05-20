from manim import *
from manim_slides import Slide
import numpy as np
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY
)
from helpers import create_modern_box, create_uniform_arrow


class Autoscaling(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("Autoscaling in Kubernetes", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Pods und Nodes dynamisch anpassen", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(title, shift=UP*0.2), FadeIn(subtitle, shift=UP*0.2))
        self.next_slide(notes="**HPA YAML** – `autoscaling/v2`. targetRef verweist auf ein Deployment. Metrik: CPU-Auslastung > 80%. minReplicas: 3, maxReplicas: 10. HPA skaliert Pods horizontal (mehr/weniger Pods).")
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2a: HPA Konfiguration (YAML)
        # ==========================================
        t2 = Text("HPA Konfiguration", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        hpa_code = Code(code_file="kubernetes/hpa.yaml", language="yaml", background="window").scale(0.6).center()
        self.play(FadeIn(hpa_code, shift=UP*0.2))
        self.next_slide(notes="**HPA in Aktion** – HPA beobachtet das ReplicaSet (3 Pods). Solange die CPU-Auslastung unter 80% bleibt, wird nicht eingegriffen.")
        self.play(FadeOut(hpa_code))

        # ==========================================
        # SLIDE 2b: HPA in Aktion
        # ==========================================
        t2b = Text("HPA in Aktion", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2b))

        hpa = create_modern_box("HPA", width=2.0, height=1.0, color=K8S_BLUE).shift(UP*1.8)
        rs_box = RoundedRectangle(width=8.5, height=2.5, corner_radius=0.2, color=K8S_BLUE, stroke_width=2, fill_color=K8S_BLUE, fill_opacity=0.05).shift(DOWN*0.5)
        rs_label = Text("ReplicaSet", font_size=20, color=K8S_BLUE, weight=BOLD).next_to(rs_box, UP, buff=0.2).align_to(rs_box, LEFT)
        watch_arrow = create_uniform_arrow(hpa.get_bottom(), rs_box.get_top(), color=TEXT_MUTED)

        p1 = create_modern_box("Pod 1", width=1.2, height=0.8, color=NODE_GREEN, font_size=14)
        p2 = create_modern_box("Pod 2", width=1.2, height=0.8, color=NODE_GREEN, font_size=14)
        p3 = create_modern_box("Pod 3", width=1.2, height=0.8, color=NODE_GREEN, font_size=14)
        pods = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.3).move_to(rs_box.get_center())

        self.play(DrawBorderThenFill(rs_box), Write(rs_label))
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.2) for p in pods], lag_ratio=0.15))
        self.play(DrawBorderThenFill(hpa[0]), Write(hpa[1]), GrowArrow(watch_arrow))
        self.next_slide(notes="**CPU Alert** – Traffic steigt, CPU > 80%. HPA berechnet neue Replica-Anzahl: aktuelle Replicas × (actualMetric / targetMetric). Entscheidet auf +3 Pods zu skalieren.")

        cpu_alert = Text("High Traffic! (CPU > 80%)", font_size=16, color=CTRL_RED, weight=BOLD).next_to(hpa, RIGHT, buff=0.4)
        self.play(FadeIn(cpu_alert, shift=LEFT*0.2), hpa[0].animate.set_color(CTRL_RED))

        hpa_action = Text("+3 Pods", font_size=16, color=NODE_GREEN, weight=BOLD).next_to(watch_arrow, RIGHT, buff=0.15)
        self.play(FadeIn(hpa_action))
        self.next_slide(notes="**Scale Out** – 3 neue Pods werden gestartet (insgesamt 6). HPA wechselt zurück zu blau (normal). CPU-Last verteilt sich auf mehr Pods. Bei Lastabfall werden Pods wieder reduziert.")

        p4 = create_modern_box("Pod 4", width=1.2, height=0.8, color=NODE_GREEN, font_size=14)
        p5 = create_modern_box("Pod 5", width=1.2, height=0.8, color=NODE_GREEN, font_size=14)
        p6 = create_modern_box("Pod 6", width=1.2, height=0.8, color=NODE_GREEN, font_size=14)

        all_pods_target = VGroup(p1.copy(), p2.copy(), p3.copy(), p4, p5, p6).arrange(RIGHT, buff=0.15).move_to(rs_box.get_center())

        self.play(
            FadeOut(hpa_action),
            p1.animate.move_to(all_pods_target[0]),
            p2.animate.move_to(all_pods_target[1]),
            p3.animate.move_to(all_pods_target[2]),
            FadeIn(p4.move_to(all_pods_target[3]), shift=UP*0.2),
            FadeIn(p5.move_to(all_pods_target[4]), shift=UP*0.2),
            FadeIn(p6.move_to(all_pods_target[5]), shift=UP*0.2),
            hpa[0].animate.set_color(K8S_BLUE),
            FadeOut(cpu_alert),
            run_time=1.2
        )
        self.next_slide(notes="**VPA YAML** – `autoscaling.k8s.io/v1`. updateMode: Auto (VPA darf Ressourcen ändern). ContainerPolicy mit min/max Limits. VPA skaliert vertikal (CPU/RAM pro Pod).")

        self.play(
            FadeOut(rs_box), FadeOut(rs_label),
            FadeOut(p1), FadeOut(p2), FadeOut(p3),
            FadeOut(p4), FadeOut(p5), FadeOut(p6),
            FadeOut(hpa), FadeOut(watch_arrow)
        )

        # ==========================================
        # SLIDE 3a: VPA Konfiguration (YAML)
        # ==========================================
        t3 = Text("VPA Konfiguration", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        vpa_code = Code(code_file="kubernetes/vpa.yaml", language="yaml", background="window").scale(0.6).center()
        self.play(FadeIn(vpa_code, shift=UP*0.2))
        self.next_slide(notes="**VPA in Aktion** – Pod mit CPU: 250m, RAM: 256Mi ist zu klein dimensioniert. VPA beobachtet Ressourcen-Nutzung und erkennt Engpässe.")
        self.play(FadeOut(vpa_code))

        # ==========================================
        # SLIDE 3b: VPA in Aktion
        # ==========================================
        t3b = Text("VPA in Aktion", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3b))

        vpa = create_modern_box("VPA", width=2.0, height=1.0, color=STORE_YELLOW).shift(UP*1.8)
        self.play(DrawBorderThenFill(vpa[0]), Write(vpa[1]))

        small_pod_bg = RoundedRectangle(width=2.8, height=1.6, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_color=NODE_GREEN, fill_opacity=BG_BOX_OPACITY)
        small_t1 = Text("Pod", font_size=18, color=TEXT_LIGHT, weight=BOLD)
        small_t2 = Text("CPU: 250m\nRAM: 256Mi", font_size=14, color=TEXT_MUTED, line_spacing=1.2)
        small_text = VGroup(small_t1, small_t2).arrange(DOWN, buff=0.2).move_to(small_pod_bg)
        small_g = VGroup(small_pod_bg, small_text).shift(DOWN*0.5)

        self.play(FadeIn(small_g, shift=UP*0.2))
        self.next_slide(notes="**OOMKilled** – Pod läuft aus Speicher (Out Of Memory, OOM). VPA analysiert die tatsächliche Nutzung und empfiehlt neue Ressourcen-Werte.")

        analyze_text = Text("OOMKilled!", font_size=16, color=CTRL_RED, weight=BOLD).next_to(vpa, RIGHT, buff=0.4)
        vpa_arrow = create_uniform_arrow(vpa.get_bottom(), small_g.get_top(), color=STORE_YELLOW)

        self.play(FadeIn(analyze_text, shift=LEFT*0.2), GrowArrow(vpa_arrow))
        self.next_slide(notes="**VPA Resize** – Pod wurde auf CPU: 500m, RAM: 1Gi hochgesetzt. VPA evictiert den Pod und startet ihn mit neuen Ressourcen. ![VPA erfordert Pod-Neustart]")

        big_pod_bg = RoundedRectangle(width=4.2, height=2.4, corner_radius=0.2, color=NODE_GREEN, stroke_width=2, fill_color=NODE_GREEN, fill_opacity=BG_BOX_OPACITY)
        big_t1 = Text("Pod", font_size=22, color=TEXT_LIGHT, weight=BOLD)
        big_t2 = Text("CPU: 500m\nRAM: 1Gi", font_size=16, color=TEXT_LIGHT, line_spacing=1.2)
        big_text = VGroup(big_t1, big_t2).arrange(DOWN, buff=0.3).move_to(big_pod_bg)
        big_g = VGroup(big_pod_bg, big_text).move_to(small_g)

        self.play(Transform(small_g, big_g), FadeOut(analyze_text), FadeOut(vpa_arrow), run_time=1.0)
        self.next_slide(notes="**Cluster Autoscaler YAML** – Läuft als Deployment im **kube-system** Namespace (System-Komponenten). `--nodes=1:10:default-worker-asg` definiert min/max Nodes und die **ASG** (Auto Scaling Group). CA skaliert Nodes, nicht Pods.")

        self.play(FadeOut(small_g), FadeOut(vpa))

        # ==========================================
        # SLIDE 4a: Cluster Autoscaler Konfiguration (YAML)
        # ==========================================
        t4 = Text("Cluster Autoscaler Konfiguration", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4))

        ca_code = Code(code_file="kubernetes/cluster-autoscaler.yaml", language="yaml", background="window").scale(0.6).center()
        self.play(FadeIn(ca_code, shift=UP*0.2))
        self.next_slide(notes="**CA in Aktion** – 2 Nodes mit jeweils 2 Pods. Beide Nodes sind voll ausgelastet. Der Cluster Autoscaler beobachtet Pending Pods.")
        self.play(FadeOut(ca_code))

        # ==========================================
        # SLIDE 4b: Cluster Autoscaler in Aktion
        # ==========================================
        t4b = Text("Cluster Autoscaler in Aktion", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4b))

        ca = create_modern_box("Cluster\nAutoscaler", width=2.5, height=1.2, color=K8S_BLUE).shift(UP * 2.2)
        cluster_box = RoundedRectangle(width=10.5, height=4.0, corner_radius=0.2, color=BOX_GRAY, stroke_width=2, fill_opacity=0.05).shift(DOWN * 1.0)
        cluster_label = Text("Cloud Provider Infrastructure", font_size=18, color=TEXT_MUTED, weight=BOLD).next_to(cluster_box, UP, buff=0.2).align_to(cluster_box, LEFT)

        def create_busy_node(name, color=BOX_GRAY):
            node = create_modern_box(name, width=2.6, height=2.4, color=color)
            node[1].next_to(node[0].get_top(), DOWN, buff=0.15)
            p_busy = VGroup(*[
                create_modern_box("Pod", width=1.0, height=0.6, color=K8S_BLUE, font_size=10)
                for _ in range(2)
            ]).arrange(RIGHT, buff=0.1).next_to(node[0].get_bottom(), UP, buff=0.3)
            return VGroup(node, p_busy)

        n1 = create_busy_node("Node 1")
        n2 = create_busy_node("Node 2")
        nodes = VGroup(n1, n2).arrange(RIGHT, buff=0.8).move_to(cluster_box.get_center() + LEFT * 1.0)

        self.play(Create(ca), Create(cluster_box), Write(cluster_label))
        self.play(FadeIn(nodes, shift=UP*0.2))
        self.next_slide(notes="**Pending Pod** – Ein weiterer Pod kann nicht platziert werden (keine freien Ressourcen auf Nodes). CA erkennt Pending Pods und fordert eine neue Node beim Cloud-Provider an.")

        pending_pod = create_modern_box("Pod\n(Pending)", width=1.6, height=0.9, color=STORE_YELLOW, font_size=14).move_to(LEFT * 5 + UP * 2.2)
        wait_arrow = create_uniform_arrow(pending_pod.get_right(), ca.get_left(), color=STORE_YELLOW)
        self.play(FadeIn(pending_pod, shift=RIGHT*0.3), GrowArrow(wait_arrow))

        api_call = Text("API: Requesting New Node...", font_size=15, color=K8S_BLUE, weight=BOLD).next_to(ca, RIGHT, buff=0.5)
        self.play(Write(api_call))
        self.next_slide(notes="**Node 3 hinzugefügt** – Cloud-Provider stellt neue VM bereit, CA registriert sie als Node 3 im Cluster. Nodes werden von 2 auf 3 erhöht.")

        n3 = create_modern_box("Node 3", width=2.6, height=2.4, color=NODE_GREEN)
        n3[1].next_to(n3[0].get_top(), DOWN, buff=0.15)

        all_nodes_target = VGroup(n1.copy(), n2.copy(), n3).arrange(RIGHT, buff=0.4).move_to(cluster_box.get_center())

        self.play(
            n1.animate.move_to(all_nodes_target[0]),
            n2.animate.move_to(all_nodes_target[1]),
            FadeIn(n3.move_to(all_nodes_target[2]), shift=LEFT*0.3),
            FadeOut(api_call),
            run_time=1.2
        )
        self.next_slide(notes="**Pod scheduled** – Der Pending Pod wurde auf Node 3 geplant und läuft (grün). Success! Bei niedriger Auslastung skaliert CA die Nodes wieder herunter (scale-down).")

        scheduled_pod = create_modern_box("Pod", width=1.8, height=0.8, color=NODE_GREEN, font_size=14).next_to(n3[0].get_bottom(), UP, buff=0.4)

        self.play(Transform(pending_pod, scheduled_pod), FadeOut(wait_arrow), run_time=1.2)
        success_msg = Text("Scaled successfully!", font_size=20, color=NODE_GREEN).next_to(cluster_box, DOWN, buff=0.3)
        self.play(FadeIn(success_msg))
        self.next_slide(notes="**Fazit** – HPA + VPA + CA = vollelastische Infrastruktur. HPA: horizontale Pod-Skalierung. VPA: vertikale Pod-Skalierung. CA: Node-Skalierung. Zusammen ermöglichen sie automatische Anpassung an Last.")

        # ==========================================
        # SLIDE 5: Conclusion
        # ==========================================
        self.play(*[FadeOut(m) for m in self.mobjects if m != title])
        conclusion = Text("HPA + VPA + CA = Vollelastische Infrastruktur", font_size=BODY_SIZE + 4, color=NODE_GREEN, weight=BOLD).center()
        self.play(Transform(title, conclusion))
        self.next_slide()

from manim import *
from manim_slides import Slide
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY, FLOW_COLOR
)
from helpers import create_modern_box, create_uniform_arrow, create_uniform_double_arrow


class ClusterArchitektur(Slide):
    def construct(self):
        
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("Cluster-Struktur & Architektur", font_size=TITLE_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=1.0)
        subtitle = Text("Control Plane vs. Worker Nodes", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        # State of the art intro: Draw borders of text, then fill
        self.play(Write(title, run_time=1.5), FadeIn(subtitle, shift=UP*0.5, run_time=1.5))
        self.next_slide()
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Control Plane vs. Data Plane
        # ==========================================
        t2 = Text("Control Plane vs. Data Plane", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        # Control Plane Box 
        cp_bg = RoundedRectangle(corner_radius=0.3, width=4.5, height=4.5, color=K8S_BLUE, stroke_width=1, fill_opacity=0.05).shift(LEFT*3.7)
        cp_label = Text("Control Plane", font_size=24, color=K8S_BLUE, weight=BOLD).next_to(cp_bg, UP, buff=0.2)

        cp_api = create_modern_box("API Server", width=1.8, height=0.8, color=K8S_BLUE).move_to(cp_bg.get_center() + UP*1.0)
        cp_etcd = create_modern_box("etcd", width=1.2, height=0.6, color=STORE_YELLOW, font_size=14).move_to(cp_bg.get_center() + DOWN*1.0 + LEFT*1.2)
        cp_sched = create_modern_box("Scheduler", width=1.4, height=0.6, color=NODE_GREEN, font_size=14).move_to(cp_bg.get_center() + DOWN*1.0 + RIGHT*1.2)

        l1 = Line(cp_etcd.get_top(), cp_api.get_bottom(), color=TEXT_MUTED, stroke_width=2).set_z_index(-1)
        l2 = Line(cp_sched.get_top(), cp_api.get_bottom(), color=TEXT_MUTED, stroke_width=2).set_z_index(-1)

        cp_group = VGroup(cp_bg, cp_label, l1, l2, cp_api, cp_etcd, cp_sched)

        # Worker Nodes Box 
        dp_bg = RoundedRectangle(corner_radius=0.3, width=4.5, height=4.5, color=NODE_GREEN, stroke_width=1, fill_opacity=0.05).shift(RIGHT*3.7)
        dp_label = Text("Worker Nodes", font_size=24, color=NODE_GREEN, weight=BOLD).next_to(dp_bg, UP, buff=0.2)
        
        node1 = create_modern_box("Node 1\n(Kubelet)", width=1.2, height=1.5, color=NODE_GREEN, font_size=14)
        node2 = create_modern_box("Node 2\n(Kubelet)", width=1.2, height=1.5, color=NODE_GREEN, font_size=14)
        node3 = create_modern_box("Node 3\n(Kubelet)", width=1.2, height=1.5, color=NODE_GREEN, font_size=14)
        
        nodes = VGroup(node1, node2, node3).arrange(RIGHT, buff=0.25).move_to(dp_bg.get_center())
        dp_group = VGroup(dp_bg, dp_label, nodes)

        # Side labels instead of center arrow
        cp_sub = Text("Steuerung", font_size=22, color=TEXT_MUTED, weight=BOLD).next_to(cp_bg, DOWN, buff=0.3)
        dp_sub = Text("Ausführung", font_size=22, color=TEXT_MUTED, weight=BOLD).next_to(dp_bg, DOWN, buff=0.3)

        # Modern animation: Lagged start for components inside the boxes
        self.play(DrawBorderThenFill(cp_bg), DrawBorderThenFill(dp_bg), Write(cp_label), Write(dp_label))
        self.play(
            LaggedStart(FadeIn(cp_api, shift=UP), FadeIn(cp_etcd, shift=UP), FadeIn(cp_sched, shift=UP), Create(l1), Create(l2), lag_ratio=0.15),
            LaggedStart(FadeIn(node1, shift=UP), FadeIn(node2, shift=UP), FadeIn(node3, shift=UP), lag_ratio=0.15),
        )
        self.play(FadeIn(cp_sub, shift=UP*0.2), FadeIn(dp_sub, shift=UP*0.2))
        self.next_slide()

        # ==========================================
        # SLIDE 3: Control Plane Deep Dive
        # ==========================================
        self.play(FadeOut(dp_group), FadeOut(cp_sub), FadeOut(dp_sub), FadeOut(cp_group))
        t3 = Text("Control Plane: Das Herzstück", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        # Shifted rack down slightly to give the architecture title more breathing room
        cp_rack = RoundedRectangle(corner_radius=0.3, width=10.0, height=5.5, color=K8S_BLUE, stroke_width=1, fill_opacity=0.03).move_to(DOWN*0.4)
        cp_rack_title = Text("Control Plane Architecture", font_size=20, color=K8S_BLUE, weight=BOLD).next_to(cp_rack, UP, buff=0.2).align_to(cp_rack, LEFT)

        api_box = create_modern_box("API Server", width=3.0, height=1.2, color=K8S_BLUE, font_size=24).move_to(cp_rack.get_center() + UP*1.0)
        api_box.set_z_index(2)

        etcd_box = create_modern_box("etcd\n(Key-Value Store)", width=3.0, height=1.0, color=STORE_YELLOW).move_to(cp_rack.get_center() + DOWN*1.5)
        sched_box = create_modern_box("Scheduler", width=2.4, height=1.0, color=NODE_GREEN).move_to(cp_rack.get_center() + LEFT*3.2 + UP*1.0)
        cm_box = create_modern_box("Controller\nManager", width=2.4, height=1.0, color=CTRL_RED).move_to(cp_rack.get_center() + RIGHT*3.2 + UP*1.0)

        # Arrows pushed to background
        arrow_etcd = create_uniform_double_arrow(etcd_box.get_top(), api_box.get_bottom(), z_index=1)
        arrow_sched = create_uniform_double_arrow(sched_box.get_right(), api_box.get_left(), z_index=1)
        arrow_cm = create_uniform_double_arrow(cm_box.get_left(), api_box.get_right(), z_index=1)

        self.play(FadeIn(cp_rack), Write(cp_rack_title))
        self.play(DrawBorderThenFill(api_box))
        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(etcd_box), GrowArrow(arrow_etcd)),
                AnimationGroup(DrawBorderThenFill(sched_box), GrowArrow(arrow_sched)),
                AnimationGroup(DrawBorderThenFill(cm_box), GrowArrow(arrow_cm)),
                lag_ratio=0.3
            )
        )
        self.next_slide()

        # ==========================================
        # SLIDE 4: Worker Node Deep Dive
        # ==========================================
        self.play(
            *[FadeOut(m) for m in [cp_rack, cp_rack_title, api_box, etcd_box, sched_box, cm_box, arrow_etcd, arrow_sched, arrow_cm]]
        )
        t4 = Text("Worker Node: Die Muskeln", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4))

        # Shifted rack down and increased height to 5.8 to fit the network routing under the pods
        rack = RoundedRectangle(corner_radius=0.3, width=9.5, height=5.8, color=NODE_GREEN, stroke_width=1, fill_opacity=0.03).move_to(DOWN*0.4)
        rack_title = Text("Worker Node Architecture", font_size=20, color=NODE_GREEN, weight=BOLD).next_to(rack, UP, buff=0.2).align_to(rack, LEFT)

        # Top Layer: Agents - shifted slightly down to maintain margins inside the lowered rack
        kubelet = create_modern_box("Kubelet\n(Node Agent)", width=3.0, height=1.0, color=NODE_GREEN).move_to(rack.get_center() + UP*1.4 + LEFT*2.0)
        proxy = create_modern_box("Kube-Proxy\n(Networking)", width=3.0, height=1.0, color=K8S_BLUE).move_to(rack.get_center() + UP*1.4 + RIGHT*2.0)
        
        # Middle Layer: Runtime
        runtime = create_modern_box("Container Runtime\n(containerd, CRI-O)", width=4.0, height=1.0, color=STORE_YELLOW).move_to(rack.get_center() + DOWN*0.4 + LEFT*2.0)
        
        # Bottom Layer: Pods
        pod1 = create_modern_box("Pod (App A)", width=2.4, height=0.8, color=NODE_GREEN).move_to(rack.get_center() + DOWN*2.0 + LEFT*3.5)
        pod2 = create_modern_box("Pod (App B)", width=2.4, height=0.8, color=NODE_GREEN).move_to(rack.get_center() + DOWN*2.0 + LEFT*0.5)

        # Connections: Kubelet watches/pulls from the API server
        api_conn = DashedLine(kubelet.get_top(), rack.get_top() + LEFT*2.0, color=FLOW_COLOR).add_tip()
        conn_label = Text("Watch API for Pod Specs", font_size=16, color=FLOW_COLOR).next_to(api_conn, RIGHT, buff=0.2)
        
        kubelet_runtime_arrow = create_uniform_arrow(kubelet.get_bottom(), runtime.get_top())
        runtime_pod_arrow1 = create_uniform_arrow(runtime.get_bottom() + LEFT*1.5, pod1.get_top())
        runtime_pod_arrow2 = create_uniform_arrow(runtime.get_bottom() + RIGHT*1.5, pod2.get_top())

        # Proxy routing visual - Orthogonal Network Bus underneath the Pods to avoid crossing the runtime box
        bus_y = pod1.get_bottom()[1] - 0.4 # Y-coordinate safely below the pods
        corner_pt = np.array([proxy.get_center()[0], bus_y, 0])
        
        # Drop line from proxy
        proxy_drop = DashedLine(proxy.get_bottom(), corner_pt, color=K8S_BLUE, stroke_opacity=0.7)
        
        # Connect to Pod 2
        bus_pt2 = np.array([pod2.get_center()[0], bus_y, 0])
        bus_line1 = DashedLine(corner_pt, bus_pt2, color=K8S_BLUE, stroke_opacity=0.7)
        up_pod2 = DashedLine(bus_pt2, pod2.get_bottom(), color=K8S_BLUE, stroke_opacity=0.7).add_tip()
        
        # Connect to Pod 1
        bus_pt1 = np.array([pod1.get_center()[0], bus_y, 0])
        bus_line2 = DashedLine(bus_pt2, bus_pt1, color=K8S_BLUE, stroke_opacity=0.7)
        up_pod1 = DashedLine(bus_pt1, pod1.get_bottom(), color=K8S_BLUE, stroke_opacity=0.7).add_tip()


        self.play(FadeIn(rack), Write(rack_title))
        self.play(FadeIn(kubelet, shift=UP*0.3), FadeIn(proxy, shift=UP*0.3))
        self.next_slide()

        # Data flow to Kubelet
        self.play(Create(api_conn), Write(conn_label))
        
        self.play(Create(kubelet_runtime_arrow), FadeIn(runtime, shift=UP*0.3))
        self.play(
            AnimationGroup(
                Create(runtime_pod_arrow1), Create(runtime_pod_arrow2),
                FadeIn(pod1, shift=UP*0.3), FadeIn(pod2, shift=UP*0.3),
                lag_ratio=0.2
            )
        )
        self.next_slide()

        self.play(Create(proxy_drop))
        self.play(
            Create(bus_line1), Create(up_pod2),
            Create(bus_line2), Create(up_pod1),
            run_time=1.5
        )
        self.next_slide()

        # ==========================================
        # SLIDE 5: Outro
        # ==========================================
        outro_1 = Text("Zusammenwirken ergibt:", font_size=BODY_SIZE, color=TEXT_MUTED)
        outro_2 = Text("Einen stabilen, skalierbaren Cluster.", font_size=TITLE_SIZE, color=NODE_GREEN, weight=BOLD)
        outro = VGroup(outro_1, outro_2).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        self.play(
            *[FadeOut(m) for m in self.mobjects if m != title],
            run_time=1.0
        )
        self.play(Transform(title, outro))
        self.wait(1)
        self.next_slide()
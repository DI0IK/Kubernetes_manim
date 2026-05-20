from manim import *
from manim_slides import Slide
from style import (
    TITLE_SIZE, SECTION_SIZE, BODY_SIZE, SMALL_SIZE,
    K8S_BLUE, NODE_GREEN, STORE_YELLOW, CTRL_RED,
    TEXT_LIGHT, TEXT_MUTED, BOX_GRAY, BG_BOX_OPACITY
)
from helpers import create_modern_box, create_uniform_arrow, create_provider_card, create_qr_code


class CloudHosting(Slide):
    def construct(self):
        # ==========================================
        # SLIDE 1: Title
        # ==========================================
        title = Text("Cloud Hosting & Infrastruktur", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Managed Kubernetes, Load Balancer und mehr", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(title, DOWN)
        
        self.play(FadeIn(title, shift=UP*0.2), FadeIn(subtitle, shift=UP*0.2))
        self.next_slide(notes="**Managed Kubernetes** – **EKS** (Elastic Kubernetes Service, Amazon), **GKE** (Google Kubernetes Engine), **AKS** (Azure Kubernetes Service). Der Cloud-Provider betreibt die Control Plane kostenlos/nach Aufwand. User managed nur Worker Nodes.")
        self.play(FadeOut(subtitle), title.animate.to_edge(UP, buff=0.4))

        # ==========================================
        # SLIDE 2: Managed Kubernetes
        # ==========================================
        t2 = Text("Managed Kubernetes", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t2))

        # Polished provider cards with brand accents
        aws = create_provider_card("EKS", "Amazon Web Services", "#FF9900")
        gcp = create_provider_card("GKE", "Google Cloud", K8S_BLUE)
        azure = create_provider_card("AKS", "Microsoft Azure", "#0078D4")

        # Evenly spacing elements
        providers = VGroup(aws, gcp, azure).arrange(RIGHT, buff=0.6).move_to(ORIGIN + DOWN*0.2)

        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(aws[0]), Write(aws[1]), FadeIn(aws[2])),
                AnimationGroup(DrawBorderThenFill(gcp[0]), Write(gcp[1]), FadeIn(gcp[2])),
                AnimationGroup(DrawBorderThenFill(azure[0]), Write(azure[1]), FadeIn(azure[2])),
                lag_ratio=0.25
            )
        )
        self.next_slide(notes="**On-Premise** – kubeadm (offizielles Setup-Tool), K3s (leichtgewichtig, für Edge/IoT), **RKE2** (Rancher Kubernetes Engine 2, gehärtet für Security), Talos (API-getrieben, minimales OS für K8s). Wahl hängt von Sicherheit & Ressourcen ab.")
        self.play(FadeOut(providers))

        # ==========================================
        # SLIDE 3: Bare Metal / On-Premise
        # ==========================================
        t3 = Text("Bare Metal / On-Premise Distributionen", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t3))

        kubeadm = create_provider_card("kubeadm", "Offizielles Tool", "#326CE5")
        k3s = create_provider_card("K3s", "Leichtgewicht", "#FF6C37")
        rke2 = create_provider_card("RKE2", "Rancher gehärtet", "#0075A8")
        talos = create_provider_card("Talos", "API-getrieben", "#5C4EE5")

        row1 = VGroup(kubeadm, k3s).arrange(RIGHT, buff=0.6).move_to(UP * 0.6)
        row2 = VGroup(rke2, talos).arrange(RIGHT, buff=0.6).move_to(DOWN * 1.8)
        bare_metal_group = VGroup(row1, row2)

        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(kubeadm[0]), Write(kubeadm[1]), FadeIn(kubeadm[2])),
                AnimationGroup(DrawBorderThenFill(k3s[0]), Write(k3s[1]), FadeIn(k3s[2])),
                AnimationGroup(DrawBorderThenFill(rke2[0]), Write(rke2[1]), FadeIn(rke2[2])),
                AnimationGroup(DrawBorderThenFill(talos[0]), Write(talos[1]), FadeIn(talos[2])),
                lag_ratio=0.2
            )
        )
        self.next_slide(notes="**LoadBalancer Service** – YAML-Definition eines Service vom Typ LoadBalancer. Port 80 wird exponiert. Der Cloud-Provider provisioniert automatisch einen externen Load Balancer (ALB, NLB, GLB).")
        self.play(FadeOut(bare_metal_group))

        # ==========================================
        # SLIDE 4: Load Balancer (Visual + Code)
        # ==========================================
        t4 = Text("Load Balancer Integration", font_size=SECTION_SIZE, color=TEXT_LIGHT).to_edge(UP, buff=0.4)
        self.play(Transform(title, t4))

        # Left Column: YAML Code
        svc_code = Code(code_file="kubernetes/service-loadbalancer.yaml", language="yaml", background="window").scale(0.75).move_to(LEFT * 3.5 + DOWN * 0.4)
        try:
            svc_code[0][0].set_fill(opacity=0.95)
        except:
            pass

        # Right Column: Architecture Elements (Clean layout spacing to prevent overlaps)
        internet = create_modern_box("Public Internet", width=3.0, height=0.8, color=BOX_GRAY).move_to(RIGHT * 3.5 + UP * 2.0)
        cloud_lb = create_modern_box("Cloud-LB\n(ALB, NLB, GLB)", width=3.0, height=1.0, color=STORE_YELLOW).move_to(RIGHT * 3.5 + UP * 0.7)
        k8s_svc = create_modern_box("Service\n(K8s internal)", width=3.0, height=1.0, color=K8S_BLUE).move_to(RIGHT * 3.5 + DOWN * 0.6)
        
        pod1 = create_modern_box("Pod 1", width=1.3, height=0.6, color=NODE_GREEN, font_size=14)
        pod2 = create_modern_box("Pod 2", width=1.3, height=0.6, color=NODE_GREEN, font_size=14)
        pods = VGroup(pod1, pod2).arrange(RIGHT, buff=0.4).move_to(RIGHT * 3.5 + DOWN * 1.9)

        # Perfect Uniform Arrows
        a1 = create_uniform_arrow(internet.get_bottom(), cloud_lb.get_top(), color=TEXT_LIGHT)
        a2 = create_uniform_arrow(cloud_lb.get_bottom(), k8s_svc.get_top(), color=TEXT_LIGHT)
        a3_1 = create_uniform_arrow(k8s_svc.get_bottom(), pod1.get_top(), color=TEXT_MUTED)
        a3_2 = create_uniform_arrow(k8s_svc.get_bottom(), pod2.get_top(), color=TEXT_MUTED)
        a3 = VGroup(a3_1, a3_2)

        # 1. First, reveal YAML code
        self.play(FadeIn(svc_code, shift=RIGHT * 0.2))
        self.next_slide(notes="**Interner Aufbau** – K8s Service (Cluster-intern) verteilt Traffic auf Pod 1 & Pod 2. Service hat eine stabile Cluster-IP, Pods sind dahinter austauschbar.")

        # 2. Render K8s internal architecture (Service & Pods)
        self.play(DrawBorderThenFill(k8s_svc[0]), Write(k8s_svc[1]))
        self.play(
            LaggedStart(
                AnimationGroup(DrawBorderThenFill(pod1[0]), Write(pod1[1]), GrowArrow(a3_1)),
                AnimationGroup(DrawBorderThenFill(pod2[0]), Write(pod2[1]), GrowArrow(a3_2)),
                lag_ratio=0.2
            )
        )
        self.next_slide(notes="**Cloud LB** – Kubernetes kommuniziert mit der Cloud-API (AWS/GCP/Azure), die automatisch einen externen Load Balancer erstellt. Der Cloud-LB leitet Traffic an den K8s-Service weiter. **ALB** (Application LB, Layer 7), **NLB** (Network LB, Layer 4), **GLB** (Google LB).")
        api_call = Text("K8s triggers Cloud API...", font_size=14, color=STORE_YELLOW, weight=BOLD).next_to(cloud_lb, UP, buff=0.15)
        self.play(FadeIn(api_call, shift=DOWN*0.1))
        
        self.play(
            DrawBorderThenFill(cloud_lb[0]), Write(cloud_lb[1]),
            GrowArrow(a2)
        )
        self.play(FadeOut(api_call))
        self.next_slide(notes="**Externer Traffic** – Public Internet → Cloud-LB → K8s Service → Pod 1/Pod 2. Der vollständige Datenpfad vom Benutzer zur Anwendung.")

        # 5. External Client traffic hits the cloud LB
        self.play(DrawBorderThenFill(internet[0]), Write(internet[1]))
        self.play(GrowArrow(a1))
        self.next_slide(notes="**Abschluss** – Vielen Dank! Fragen? QR-Code führt zur Links-Sammlung mit allen Ressourcen aus der Präsentation.")

        # ==========================================
        # SLIDE 4: Outro / Questions
        # ==========================================
        # Safely wrap up
        fade_out_group = VGroup(svc_code, internet, cloud_lb, k8s_svc, pods, a1, a2, a3)

        self.play(FadeOut(fade_out_group))
            
        final = Text("Vielen Dank!", font_size=TITLE_SIZE, color=TEXT_LIGHT, weight=BOLD)
        final_q = Text("Fragen?", font_size=BODY_SIZE, color=TEXT_MUTED).next_to(final, DOWN, buff=0.4)
        qr = create_qr_code("https://di0ik.github.io/Kubernetes_manim/links.html", scale=1.5)
        qr_label = Text("K8s Resources", font_size=14, color=TEXT_MUTED, weight=BOLD).next_to(qr, DOWN, buff=0.1)
        qr_group = Group(qr, qr_label).to_edge(DR, buff=0.5)
        
        # Merge slide title smoothly into standard middle screen
        self.play(Transform(title, final), FadeIn(final_q, shift=UP*0.2), FadeIn(qr_group, shift=UP*0.2))
        self.play(title.animate.center().scale(1.1))
        self.next_slide()

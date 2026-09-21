# Author: Semanur Biçer
# Project: Bio-Mathematical Resilience Framework
# License: Apache 2.0

import numpy as np
import matplotlib.pyplot as plt

class VisualBioMathematicalSystem:
    def __init__(self, radius=2):
        self.radius = radius
        self.hex_nodes = {}
        self.entropy_threshold = 400.0
        self._initialize_system()

    def _initialize_system(self):
        """Eksenel koordinatlarla (q, r) altıgen kafesi kurar."""
        self.hex_nodes.clear()
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2 + 1):
                self.hex_nodes[(q, r)] = {
                    'matrix_4x3': np.random.rand(4, 3), 
                    'h_bond_strength': 1.0 
                }
        print(f"[*] Hexagonal Lattice Initialized / Seeded. Total Nodes: {len(self.hex_nodes)}")

    def axial_to_cartesian(self, q, r):
        """Altıgen eksenel koordinatları 2D Cartesian (x, y) düzlemine çevirir."""
        x = np.sqrt(3) * (q + r / 2.0)
        y = (3.0 / 2.0) * r
        return x, y

    def apply_x0_input(self, input_type):
        """x0 Değişkeni: Karbonhidrat (Gürültü/Isı) vs Protein/Su (Onarım)"""
        print(f"\n[x0 Event Triggered] Input Type: {input_type.upper()}")
        for node in self.hex_nodes.values():
            if input_type == 'carbohydrate':
                noise = np.random.uniform(0.8, 1.5, (4, 3))
                node['matrix_4x3'] += noise
                node['h_bond_strength'] *= 0.65 
            elif input_type == 'protein_water':
                node['matrix_4x3'] *= 0.75 
                node['h_bond_strength'] = min(1.0, node['h_bond_strength'] * 1.4)

    def evaluate_state(self):
        total_entropy = sum(np.sum(np.abs(n['matrix_4x3'])) for n in self.hex_nodes.values())
        avg_bond = np.mean([n['h_bond_strength'] for n in self.hex_nodes.values()])
        return total_entropy, avg_bond

    def run_simulation_stages(self):
        """4 Aşamayı simüle eder, Throttling kontrolü yapar ve sonuçları görselleştirir."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        stages = [
            ("Stage 1: Normal Elastic Operation", 'normal'),
            ("Stage 2: Moderate Carbohydrate Noise", 'carbohydrate'),
            ("Stage 3: Critical Stress (Throttling Zone)", 'carbohydrate'),
            ("Stage 4: Protein & Water Recovery", 'protein_water')
        ]

        for i, (title, action) in enumerate(stages):
            if i > 0 and i != 3:
                self.apply_x0_input(action)
            elif i == 3:
                self.apply_x0_input('protein_water')

            total_entropy, avg_bond = self.evaluate_state()

            # Thermal Throttling & Seeding kontrolü (Stage 3'te eşik aşılırsa tetiklenir)
            if total_entropy > self.entropy_threshold or avg_bond < 0.35:
                print(f"🚨 [Throttling Triggered at {title}] -> Executing External Seeding!")
                self._initialize_system()
                total_entropy, avg_bond = self.evaluate_state()

            # Grafik Çizimi (Altıgen Düğümler)
            ax = axes[i]
            x_coords, y_coords, colors = [], [], []
            
            for (q, r), node in self.hex_nodes.items():
                x, y = self.axial_to_cartesian(q, r)
                x_coords.append(x)
                y_coords.append(y)
                # H-Bağı sağlamlığına göre renk (1.0 = Yeşil/Sağlam, 0.0 = Kırmızı/Kırılgan)
                colors.append(node['h_bond_strength'])

            sc = ax.scatter(x_coords, y_coords, c=colors, cmap='RdYlGn', s=400, vmin=0, vmax=1, edgecolors='black')
            ax.set_title(f"{title}\nEntropy: {total_entropy:.1f} | Bond: {avg_bond:.2f}", fontsize=11, fontweight='bold')
            ax.set_aspect('equal')
            ax.axis('off')

        # Renk ölçeği (Colorbar) ekleme
        fig.colorbar(sc, ax=axes.ravel().tolist(), label='H-Bond Integrity (Elasticity)')
        plt.suptitle("Bio-Mathematical Resilience: Hexagonal Lattice Dynamics", fontsize=15, fontweight='bold')
        
        # Dosyaya kaydetme ve ekranda gösterme
        plt.savefig('resilience_lattice_simulation.png', dpi=300)
        print("\n✅ Simülasyon görseli başarıyla 'resilience_lattice_simulation.png' olarak kaydedildi!")
        plt.show()

if __name__ == "__main__":
    print("=== BIO-MATHEMATICAL RESILIENCE FRAMEWORK: VISUAL SIMULATOR ===")
    sim = VisualBioMathematicalSystem(radius=2)
    sim.run_simulation_stages()

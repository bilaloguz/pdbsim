# PD-Sim: Neuroevolutionary Prisoner's Dilemma

An advanced **Agent-Based Simulation (ABS)** exploring the evolution of cooperation, culture, and intelligence in a competitive digital ecosystem. This project models how Neural Networks (`Brain`), inheritable culture (`Ideology`), and economic pressure (`Taxes`) shape the emergence of complex societies.

---

## 🇬🇧 English Documentation

### 1. Project Overview
This simulation places autonomous agents on a 2D grid where they interact via the **Prisoner's Dilemma** game. Unlike simple rule-based models, these agents possess evolving **Neural Networks** that learn strategies over generations. They reproduce, migrate, form cultures, and eventually die, allowing "Survival of the Fittest" to select for the most successful behavioral traits.

### 2. Core Mechanics

#### 🧠 The Brain 2.0 (Neuroevolution)
Every agent possesses an **Evolvable Neural Network**:
*   **Neurogenesis:** The brain size (Hidden Neurons) is not fixed. It evolves from **2 to 20** neurons.
*   **Growth & Atrophy:** During mutation, a child can add a neuron (Growth) or lose one (Atrophy). The weights are adjusted to preserve the parent's knowledge.
*   **Brain Tax:** Intelligence is expensive (`brain_complexity_tax`). Agents must balance "Being Smart" vs "Being Efficient".
*   **Inputs (6):** `[MyPoints, MyAge, OppFame, OppHistory, Bias, Ideology]`.
*   **Outputs (4):** `[Cooperate, Defect, Move, Ignore]`.

#### 🧬 Genetics & Culture
Traits are no longer just hardcoded probabilities; they are complex biological and cultural markers:
*   **Ideology Inheritance:** Children inherit their parent's *current* Ideology (Optimism/Cynicism). This creates "Cultural Momentum"—a high-trust parent raises a high-trust child.
*   **Evolvable Memory:** `memory_capacity` is a gene (5-50 slots). Smarter agents pay higher taxes (`cognitive_tax_rate`).

#### ⚖️ Social Dynamics
*   **Ideology (Trust Model):** Agents have a "Mood" (0.0=Cynic, 1.0=Idealist). Cooperation boosts this mood; betrayal destroys it.
*   **Gossip Reliability:** Public fame is noisy. Agents might hear misinformation (`gossip_reliability`).
*   **Migration:** Overcrowded agents can pay a **Migration Tax** (`migration_tax`) to "Launch" offspring to distant lands.

#### 💰 Economic Physics
The world is governed by strict thermodynamic laws:
*   **Taxes:** Existence Tax + Cognitive Tax (Memory) + Brain Tax (Neurons).
*   **Payoff Matrix:** High temptation to defect (10) vs moderate reward for cooperation (5).

### 3. Real-Time Visualization
The simulation now runs a live dashboard with **3 Real-time Charts**:
1.  **Population Size:** Total agents alive.
2.  **Social Capital:** Compares Avg Reputation (Fame) vs Avg Trust (Ideology).
3.  **Cognitive Evolution:** Compares Avg Brain Size (Red) vs Avg Memory (Orange).

### 4. How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run Visualization (The Movie)
python3 main.py
```
---

## 🇹🇷 Türkçe Dokümantasyon

### 1. Proje Özeti
Bu simülasyon, "Tutsak İkilemi" oyunu üzerinden etkileşime giren ajanları modeller. Ajanlar, nesiller boyu öğrenen ve **Evrimleşen Sinir Ağlarına (Brain 2.0)** sahiptir. Ürerler, göç ederler, kültür oluştururlar ve ölürler.

### 2. Temel Mekanikler

#### 🧠 Beyin 2.0 (Nöroevrim)
*   **Nörogenez:** Beyin boyutu (Gizli Nöronlar) 2 ile 20 arasında değişir ve evrimleşir.
*   **Büyüme ve Körelme:** Mutasyon sırasında beyin büyüyebilir (yeni nöron) veya küçülebilir. Ebeveynin bilgisi korunur.
*   **Beyin Vergisi:** Zeki olmak pahalıdır (`brain_complexity_tax`). Ajanlar "Zeki Olmak" ile "Verimli Olmak" arasında seçim yapmalıdır.

#### 🧬 Genetik ve Kültür
*   **İdeoloji Mirası:** Çocuklar, ebeveynlerinin dünya görüşünü miras alır. Güven kültürü nesiller boyu aktarılır.
*   **Bilişsel Vergi:** Hafıza kapasitesi evrimleşir, ancak yüksek hafıza daha yüksek vergi demektir.

### 3. Görselleştirme
Canlı panelde 3 grafik bulunur:
1.  **Nüfus:** Toplam canlı ajan sayısı.
2.  **Sosyal Sermaye:** İtibar (Fame) ve Güven (Ideology) karşılaştırması.
3.  **Bilişsel Evrim:** Beyin Boyutu (Nöronlar) ve Hafıza Kapasitesi.

### 4. Nasıl Çalıştırılır
```bash
python3 main.py
```
*Görselleştirme penceresi açılır. Evrimi izleyin.*

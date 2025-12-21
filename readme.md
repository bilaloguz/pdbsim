# Prisoner's Dilemma Social Simulation / Tutsak İkilemi Sosyal Simülasyonu

An advanced **Agent-Based Simulation (ABS)** exploring the evolution of cooperation, reputation, and survival strategies in a competitive digital ecosystem. The project models how genetic traits (`DNA`), social memory (`Fame`), and economic pressure (`Taxes`) influence the emergence of altruism or selfishness.

Bir rekabetçi dijital ekosistemde işbirliği, itibar ve hayatta kalma stratejilerinin evrimini inceleyen gelişmiş bir **Ajan Tabanlı Simülasyon (ABS)**. Proje, genetik özelliklerin (`DNA`), sosyal hafızanın (`Şöhret`) ve ekonomik baskının (`Vergiler`) diğerkâmlık veya bencilliğin ortaya çıkışını nasıl etkilediğini modeller.

---

## 🇬🇧 English Documentation

### 1. Project Overview
This simulation places autonomous agents on a 2D grid where they interact via the **Prisoner's Dilemma** game. Unlike simple models, these agents have "brains" that weigh their internal genetic nature against their private experiences and the public reputation of their neighbors. The goal is to observe whether a society of cooperators can survive against "free riders" (defectors) under various economic conditions.

### 2. Core Mechanics

#### 🧬 The DNA (Genetics)
Every agent is born with a unique set of immutible traits (DNA) inherited from their parent with slight mutations:
*   **`trustworthiness` (0.0 - 1.0):** The base probability that the agent will cooperate, before considering external factors.
*   **`vengefulness` (0.0 - 1.0):** How much the agent prioritizes their *private memory* of someone over that person's *public reputation*. High vengefulness means they never forgive a personal betrayal, even if the person is famous.
*   **`social_sensitivity` (0.0 - 1.0):** How much the agent cares about reputation. A low score means they ignore what society thinks; a high score means they conform to the social norm (trusting famous people, shunning outcasts).
*   **`mobility_inclination` (0.0 - 1.0):** The likelihood of moving to a new location if lonely or dissatisfied with neighbors.
*   **`memory_capacity` (Int):** The number of past interactions the agent can remember per neighbor. Higher memory allows for better judgment but incurs a "Cognitive Tax" (brain upkeep cost).
*   **`hunger_threshold` (Points):** The point level at which the agent enters "Survival Mode".

#### 🧠 The Decision Engine
Agents are not mindless automatons. Every tick, they make a decision (`Cooperate`, `Defect`, `Move`, or `Ignore`) based on a utility function:
1.  **Survival Override:** If an agent's points drop below their `hunger_threshold`, they enter panic mode. The likelihood of **Defection** (stealing points) increases drastically, disregarding their moral DNA.
2.  **Trust Evaluation:** The agent calculates a "Trust Score" for their neighbor by blending the neighbor's public **Fame** (Social Ledger) with their own **Private Memory**.
3.  **Action:**
    *   **High Trust:** Cooperate.
    *   **Low Trust:** Defect (Pre-emptive strike).
    *   **Very Low Trust:** Move away or Ignore (Social Ostracism).
    *   **Whim:** A flat 5% chance of doing something completely random to simulate irrationality.

#### ⚖️ The Social Ledger (Reputation)
*   **Public Fame:** The society maintains a shared ledger of every agent's reputation.
*   **Gossip:** Actions are recorded but can be "noisy" based on the `gossip_reliability` setting.
*   **Decay:** Reputation isn't permanent. Fame decays every tick (`fame_decay`), forcing agents to continuously prove their worth to stay "Green" (Good).
*   **Visualization:** In the UI, **Green** agents are cooperators, **Red** are defectors, and **Yellow** are neutral/unknown.

#### 💰 Economic Physics
The world is harsh. Agents must maintain a positive point balance to survive.
*   **Payoff Matrix:**
    *   **Coop/Coop:** Both gain moderate points (Reward).
    *   **Defect/Coop:** Defector gains huge points (Temptation), Cooperator loses huge points (Sucker).
    *   **Defect/Defect:** Both lose small points (Punishment).
*   **Taxes:**
    *   **Existence Tax:** Cost of living per tick.
    *   **Cognitive Tax:** Cost proportional to `memory_capacity`. Smarter agents need more food.
    *   **Movement Tax:** Cost to move to a new cell.

### 3. File Structure
*   `main.py`: Entry point. Initializes the engine and runs the visualization loop.
*   `config.py`: Central control room. modify `payoff_matrix`, `tax_rates`, and `DNA_bounds` here.
*   `analyze.py`: Post-run analysis tool. Plots historical data (Population, Fame, Wealth) from the CSV logs.
*   `simulation/`:
    *   `agent.py`: Contains the `Agent` class and the decision logic (`decide()`).
    *   `engine.py`: Manages the game loop, turn processing, and global rules (taxes/death).
    *   `social.py`: Manages the global `SocialLedger`.
    *   `world.py`: Manages the 2D grid geometry.

### 4. Installation & Usage

**Prerequisites:** Python 3.x
**Dependencies:** `numpy`, `matplotlib`, `pandas`

1.  **Install Libraries:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Simulation:**
    ```bash
    python3 main.py
    ```
    *The visualizer window will open. Watch the evolution in real-time.*

3.  **Analyze Results:**
    After the simulation finishes (or is interrupted), run:
    ```bash
    python3 analyze.py
    ```
    *This generates graphs showing population stability and behavioral trends.*

---

## 🇹🇷 Türkçe Dokümantasyon

### 1. Proje Özeti
Bu simülasyon, "Tutsak İkilemi" (Prisoner's Dilemma) oyunu üzerinden etkileşime giren otonom ajanları 2 boyutlu bir ızgaraya yerleştirir. Basit modellerin aksine, bu ajanların içsel genetik yapılarını ("Gen"), özel deneyimlerini ve komşularının kamuya açık itibarlarını tartan "beyinleri" vardır. Amaç, çeşitli ekonomik koşullar altında işbirlikçi bir toplumun "beleşçilere" (ihanet edenlere) karşı hayatta kalıp kalamayacağını gözlemlemektir.

### 2. Temel Mekanikler

#### 🧬 DNA (Genetik)
Her ajan, ebeveyninden hafif mutasyonlarla miras aldığı benzersiz özelliklerle (DNA) doğar:
*   **`trustworthiness` (Güvenilirlik):** Dış faktörler hesaba katılmadan önce ajanın işbirliği yapma konusundaki temel eğilimi.
*   **`vengefulness` (İntikamcılık):** Ajanın bir kişi hakkındaki *özel hafızasını*, o kişinin *toplumsal itibarından* ne kadar üstün tuttuğu. Yüksek intikamcılık, kişi "ünlü" olsa bile şahsi ihanetlerin asla affedilmemesi anlamına gelir.
*   **`social_sensitivity` (Sosyal Duyarlılık):** Ajanın itibarı ne kadar önemsediği. Düşük puan toplumu umursamazlık; yüksek puan toplumsal normlara (ünlülere güvenmek, dışlanmışları yok saymak) uymak demektir.
*   **`mobility_inclination` (Hareket Eğilimi):** Yalnız kaldıysa veya komşularından memnun değilse yeni bir yere taşınma olasılığı.
*   **`memory_capacity` (Hafıza Kapasitesi):** Ajanın komşu başına hatırlayabileceği geçmiş etkileşim sayısı. Yüksek hafıza daha iyi karar vermeyi sağlar ancak "Bilişsel Vergi" (beyin bakım maliyeti) doğurur.
*   **`hunger_threshold` (Açlık Sınırı):** Ajanın "Hayatta Kalma Moduna" girdiği puan seviyesi.

#### 🧠 Karar Motoru
Ajanlar şuursuz robotlar değildir. Her turda, bir fayda fonksiyonuna (utility function) dayanarak bir karar (`İşbirliği`, `İhanet`, `Taşınma` veya `Yoksayma`) verirler:
1.  **Hayatta Kalma Baskısı (Override):** Ajanın puanları `hunger_threshold` altına düşerse panik moduna girer. Ahlaki DNA'sı ne olursa olsun, **İhanet** (puan çalma) olasılığı radikal biçimde artar.
2.  **Güven Değerlendirmesi:** Ajan, komşusunun halka açık **Şöhretini** (Sosyal Defter) kendi **Özel Hafızası** ile harmanlayarak bir "Güven Puanı" hesaplar.
3.  **Eylem:**
    *   **Yüksek Güven:** İşbirliği yap.
    *   **Düşük Güven:** İhanet et (Önleyici saldırı).
    *   **Çok Düşük Güven:** Taşın veya Yoksay (Sosyal Dışlanma - Ostracism).
    *   **Keyfekeder (Whim):** İrrasyonelliği simüle etmek için %5 şansla tamamen rastgele bir hamle yap.

#### ⚖️ Sosyal Defter (İtibar Sistemi)
*   **Kamu Şöhreti:** Toplum, her ajanın itibarı için ortak bir defter tutar.
*   **Dedikodu:** Eylemler kaydedilir ancak `gossip_reliability` ayarına bağlı olarak "parazitli" (hatalı) olabilir.
*   **Çürüme:** İtibar kalıcı değildir. Şöhret her turda azalır (`fame_decay`), bu da ajanları "Yeşil" (İyi) kalmak için kendilerini sürekli kanıtlamaya zorlar.
*   **Görselleştirme:** Arayüzde, **Yeşil** ajanlar işbirlikçi, **Kırmızı** ajanlar hain, **Sarı** ajanlar ise nötr/bilinmeyendir.

#### 💰 Ekonomik Fizik
Dünya acımasızdır. Ajanlar hayatta kalmak için pozitif bir puan bakiyesini korumalıdır.
*   **Kazanç Matrisi:**
    *   **Coop/Coop:** İkisi de orta düzeyde puan kazanır (Ödül).
    *   **Defect/Coop:** Hain büyük puan kazanır (Ayartma), İşbirlikçi büyük puan kaybeder (Enayi).
    *   **Defect/Defect:** İkisi de az puan kaybeder (Ceza).
*   **Vergiler:**
    *   **Varoluş Vergisi:** Tur başına yaşam maliyeti.
    *   **Bilişsel Vergi:** `memory_capacity` ile orantılı maliyet. Daha zeki ajanlar daha fazla yiyeceğe ihtiyaç duyar.
    *   **Hareket Vergisi:** Yeni bir kareye taşınmanın maliyeti.

### 3. Dosya Yapısı
*   `main.py`: Giriş noktası. Motoru başlatır ve görselleştirme döngüsünü çalıştırır.
*   `config.py`: Merkezi kontrol odası. `payoff_matrix`, `tax_rates` ve `DNA_bounds` ayarlarını buradan değiştirin.
*   `analyze.py`: Çalıştırma sonrası analiz aracı. CSV kayıtlarından tarihsel verileri (Nüfus, Şöhret, Zenginlik) grafiğe döker.
*   `simulation/`:
    *   `agent.py`: `Agent` sınıfını ve karar mantığını (`decide()`) içerir.
    *   `engine.py`: Oyun döngüsünü, tur işlemlerini ve küresel kuralları (vergiler/ölüm) yönetir.
    *   `social.py`: Küresel `SocialLedger` yapısını yönetir.
    *   `world.py`: 2 boyutlu ızgara geometrisini yönetir.

### 4. Kurulum ve Kullanım

**Gereksinimler:** Python 3.x
**Kütüphaneler:** `numpy`, `matplotlib`, `pandas`

1.  **Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Simülasyonu Başlatın:**
    ```bash
    python3 main.py
    ```
    *Görselleştirme penceresi açılacaktır. Evrimi gerçek zamanlı izleyin.*

3.  **Sonuçları Analiz Edin:**
    Simülasyon bittikten (veya durdurulduktan) sonra şunu çalıştırın:
    ```bash
    python3 analyze.py
    ```
    *Bu komut, nüfus istikrarını ve davranışsal eğilimleri gösteren grafikler oluşturur.*
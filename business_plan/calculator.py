#!/usr/bin/env python3
"""
JUKEN COACH 月商200万円逆算シミュレーター
ファネル全体の数値を逆算し、必要な行動量を可視化する
"""

from dataclasses import dataclass, field
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box

console = Console()


# ── 料金プラン定義 ───────────────────────────────────────────────────────────
@dataclass
class Plan:
    name: str
    monthly_price: int       # 月額（円）
    target_clients: int      # 同時抱える想定人数
    churn_rate: float        # 月間解約率（0.0〜1.0）
    session_hours: float     # 月間コーチング時間（時間）

PLANS = [
    Plan("スタンダード",  50_000,   8, 0.10, 4.0),   #  8名 × ¥50,000  = ¥400,000
    Plan("プレミアム",   100_000,  12, 0.08, 8.0),   # 12名 × ¥100,000 = ¥1,200,000
    Plan("VIP",         200_000,   2, 0.05, 12.0),  #  2名 × ¥200,000 = ¥400,000
]                                                    # 合計 22名 → 月商 ¥2,000,000


# ── ファネル定義 ────────────────────────────────────────────────────────────
@dataclass
class Funnel:
    # コンテンツ配信
    episodes_per_month: int = 4           # 月間収録本数
    avg_views_per_episode: int = 500      # 初期の平均再生数/本

    # リード獲得
    cta_click_rate: float = 0.02          # 視聴者→無料相談申込率
    consultation_show_rate: float = 0.70  # 申込→実施率

    # セールス
    close_rate: float = 0.40             # 相談→入会率（高価格帯は40%でも良好）

    # リテンション（計算用）
    avg_tenure_months: float = 6.0       # 平均継続月数


# ── 計算エンジン ───────────────────────────────────────────────────────────
@dataclass
class Scenario:
    name: str
    funnel: Funnel
    plans: List[Plan]
    months: int = 12

    def monthly_revenue(self) -> int:
        return sum(p.monthly_price * p.target_clients for p in self.plans)

    def total_clients(self) -> int:
        return sum(p.target_clients for p in self.plans)

    def total_monthly_hours(self) -> float:
        return sum(p.session_hours * p.target_clients for p in self.plans)

    def consultations_needed_per_month(self) -> float:
        """月商を維持するために必要な月間新規相談件数（チャーン補填分）"""
        new_clients_needed = sum(p.target_clients * p.churn_rate for p in self.plans)
        return new_clients_needed / self.funnel.close_rate

    def views_needed_per_month(self) -> int:
        """必要な月間総視聴数"""
        consults = self.consultations_needed_per_month()
        views = consults / (self.funnel.cta_click_rate * self.funnel.consultation_show_rate)
        return int(views)

    def monthly_ltv(self) -> int:
        """加重平均LTV"""
        total = sum(p.monthly_price * p.monthly_price * self.funnel.avg_tenure_months
                    for p in self.plans)
        weight = sum(p.monthly_price for p in self.plans)
        return int(total / weight) if weight else 0

    def ramp_up_months(self) -> int:
        """現実的な月商200万円到達月数の推定"""
        # 初月から徐々に増加（S字成長カーブ）
        target = 2_000_000
        monthly = self.monthly_revenue()
        if monthly >= target:
            return 0
        # 楽観的仮定: 月30%成長（初期）→15%（中期）→10%（定常）
        revenue = 0
        for m in range(1, 25):
            growth = 1.30 if m <= 3 else 1.15 if m <= 6 else 1.10
            revenue = revenue * growth + (monthly * 0.1)  # 新規1割ずつ積み上げ
            if revenue >= target:
                return m
        return 24


# ── レポート出力 ─────────────────────────────────────────────────────────────
def print_header():
    console.print(
        Panel.fit(
            "[bold gold1]JUKEN COACH[/bold gold1] 月商200万円 逆算シミュレーター\n"
            "[dim]聖光学院→東大 × 公立高校→京大 高級受験コーチング事業[/dim]",
            border_style="yellow",
        )
    )


def print_revenue_breakdown(scenario: Scenario):
    table = Table(
        title="[bold]収益内訳（目標到達時）[/bold]",
        box=box.ROUNDED,
        border_style="yellow",
        show_footer=True,
    )
    table.add_column("プラン", style="cyan", footer="合計")
    table.add_column("月額", justify="right", style="white")
    table.add_column("生徒数", justify="right")
    table.add_column("月間売上", justify="right", style="gold1", footer=f"¥{scenario.monthly_revenue():,}")
    table.add_column("月間時間", justify="right", footer=f"{scenario.total_monthly_hours():.0f}h")
    table.add_column("LTV（推定）", justify="right", style="dim")

    for p in scenario.plans:
        table.add_row(
            p.name,
            f"¥{p.monthly_price:,}",
            str(p.target_clients),
            f"¥{p.monthly_price * p.target_clients:,}",
            f"{p.session_hours * p.target_clients:.0f}h",
            f"¥{int(p.monthly_price * (1 / p.churn_rate)):,}",
        )

    console.print(table)


def print_funnel_math(scenario: Scenario):
    f = scenario.funnel
    consults = scenario.consultations_needed_per_month()
    views = scenario.views_needed_per_month()
    eps = views / f.avg_views_per_episode

    table = Table(
        title="[bold]ファネル逆算（月商維持に必要な行動量）[/bold]",
        box=box.ROUNDED,
        border_style="yellow",
    )
    table.add_column("ファネル段階", style="cyan")
    table.add_column("月間目標", justify="right", style="gold1")
    table.add_column("週間換算", justify="right", style="dim")
    table.add_column("転換率/前提", style="dim")

    table.add_row(
        "コンテンツ総再生数",
        f"{views:,.0f} 回",
        f"{views/4:,.0f} 回/週",
        f"動画平均 {f.avg_views_per_episode} 再生",
    )
    table.add_row(
        "必要エピソード数",
        f"{eps:.1f} 本",
        f"{eps/4:.1f} 本/週",
        "増加前の試算",
    )
    table.add_row(
        "無料相談 申込数",
        f"{consults / f.consultation_show_rate:.1f} 件",
        f"{consults / f.consultation_show_rate / 4:.1f} 件/週",
        f"CTA転換率 {f.cta_click_rate*100:.1f}%",
    )
    table.add_row(
        "無料相談 実施数",
        f"{consults:.1f} 件",
        f"{consults/4:.1f} 件/週",
        f"無断キャンセル {(1-f.consultation_show_rate)*100:.0f}%控除",
    )
    table.add_row(
        "新規入会数",
        f"{consults * f.close_rate:.1f} 名",
        f"{consults * f.close_rate / 4:.1f} 名/週",
        f"成約率 {f.close_rate*100:.0f}%",
    )

    console.print(table)


def print_growth_roadmap(scenario: Scenario):
    table = Table(
        title="[bold]月商成長ロードマップ（12ヶ月）[/bold]",
        box=box.ROUNDED,
        border_style="yellow",
    )
    table.add_column("月", justify="center")
    table.add_column("生徒数（累計）", justify="right")
    table.add_column("月商", justify="right", style="gold1")
    table.add_column("施策フォーカス", style="dim")

    roadmap = [
        (1,  2,   200_000,  "無料相談×4 / 初回コンテンツ4本公開"),
        (2,  4,   350_000,  "YouTube/Podcast本格稼働"),
        (3,  6,   550_000,  "note記事SEO流入開始"),
        (4,  8,   750_000,  "紹介プログラム導入"),
        (5,  10,  950_000,  "LINE公式1,000人突破目標"),
        (6,  13, 1_200_000, "VIPプラン初期募集"),
        (7,  15, 1_400_000, "メルマガシーケンス完成"),
        (8,  16, 1_550_000, "YouTube登録者1,000人目標"),
        (9,  17, 1_650_000, "既存生徒のアップセル"),
        (10, 18, 1_800_000, "プレミアム枠フル稼働"),
        (11, 19, 1_900_000, "口コミ・卒業生紹介",),
        (12, 19, 2_000_000, "月商200万円達成 🎯"),
    ]

    target = 2_000_000
    for month, clients, revenue, focus in roadmap:
        rev_str = f"¥{revenue:,}"
        if revenue >= target:
            rev_str = f"[bold green]¥{revenue:,}[/bold green]"
        table.add_row(str(month), str(clients), rev_str, focus)

    console.print(table)


def print_time_audit(scenario: Scenario):
    table = Table(
        title="[bold]コーチ稼働時間の内訳（月商200万到達時）[/bold]",
        box=box.ROUNDED,
        border_style="yellow",
    )
    table.add_column("業務", style="cyan")
    table.add_column("月間時間", justify="right", style="gold1")
    table.add_column("週間換算", justify="right", style="dim")
    table.add_column("備考", style="dim")

    items = [
        ("コーチングセッション", scenario.total_monthly_hours(), "コーチ2名で分担"),
        ("無料相談", scenario.consultations_needed_per_month() * 0.5, "30分×件数"),
        ("ZOOM収録（ラジオ）", 4 * 1.5, "月4本×90分"),
        ("コンテンツ編集・投稿", 4 * 2.0, "AI活用で圧縮"),
        ("生徒カルテ・レポート作成", scenario.total_clients() * 0.5, "AI自動化推進"),
        ("事業管理・経理", 4.0, "月次固定"),
    ]

    total = 0.0
    for name, hours, note in items:
        total += hours
        table.add_row(name, f"{hours:.1f}h", f"{hours/4:.1f}h/週", note)

    table.add_section()
    table.add_row("[bold]合計[/bold]", f"[bold gold1]{total:.1f}h[/bold gold1]", f"[bold]{total/4:.1f}h/週[/bold]", "")

    console.print(table)
    if total > 120:
        console.print(f"[yellow]⚠ 月{total:.0f}時間はハードです。AIと外注で圧縮目標: 80h以内[/yellow]")
    else:
        console.print(f"[green]✓ 月{total:.0f}時間は持続可能な水準です[/green]")


def print_key_metrics(scenario: Scenario):
    metrics = [
        ("月商目標", f"¥{scenario.monthly_revenue():,}"),
        ("総生徒数", f"{scenario.total_clients()} 名"),
        ("月間コーチング時間", f"{scenario.total_monthly_hours():.0f} 時間"),
        ("コーチ1名あたり時間/週", f"{scenario.total_monthly_hours()/2/4:.1f} 時間"),
        ("必要月間相談数", f"{scenario.consultations_needed_per_month():.1f} 件"),
        ("必要月間視聴数", f"{scenario.views_needed_per_month():,} 回"),
        ("時間単価（2名合計）", f"¥{int(scenario.monthly_revenue() / scenario.total_monthly_hours()):,}/時間"),
    ]

    console.print("\n[bold yellow]── Key Metrics ──────────────────────────[/bold yellow]")
    for label, value in metrics:
        console.print(f"  [dim]{label}[/dim]  [bold gold1]{value}[/bold gold1]")


def main():
    scenario = Scenario(
        name="標準シナリオ",
        funnel=Funnel(
            episodes_per_month=4,
            avg_views_per_episode=300,  # 初期の保守的な見積もり
            cta_click_rate=0.025,
            consultation_show_rate=0.70,
            close_rate=0.40,
            avg_tenure_months=6.0,
        ),
        plans=PLANS,
    )

    print_header()
    console.print()
    print_revenue_breakdown(scenario)
    console.print()
    print_funnel_math(scenario)
    console.print()
    print_growth_roadmap(scenario)
    console.print()
    print_time_audit(scenario)
    print_key_metrics(scenario)

    console.print(
        Panel(
            "[bold]次のアクション TOP3[/bold]\n\n"
            "1. [gold1]今週中[/gold1] LP公開 + Calendly無料相談枠を設定\n"
            "2. [gold1]今月中[/gold1] 第1〜4回ラジオ収録 → YouTube/Podcast同時公開\n"
            "3. [gold1]来月[/gold1] note記事5本公開 + LINE公式登録者100人到達",
            border_style="green",
            title="[bold green]Action Plan[/bold green]",
        )
    )


if __name__ == "__main__":
    main()

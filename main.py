import json
import datetime
import traceback
from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, DataTable, Header, Footer
from textual import work
from req import get_gszzl, get_industry


# 读取配置
data = json.load(open("./CONFIG.json", "r"))
fund_codes = data["funds"]
refresh_interval = data.get("refresh_interval", 5)
top_k = data.get("top-K", 30)
retry = data.get("req-retry", 10)


class FundApp(App):
    """基金监控应用"""
    
    CSS = """
    Screen {
        background: #121212;
    }

    TabbedContent {
        height: 1fr;
        margin: 0;
    }

    /* 让表格撑满整个标签页 */
    TabPane {
        padding: 0;
        height: 1fr;
    }

    DataTable {
        height: 1fr;
        border: tall #333;
        background: #1a1a1a;
    }

    /* 斑马纹颜色微调 */
    DataTable > .datatable--even-row {
        background: #242424;
    }

    /* 底部状态栏样式 */
    Footer {
        background: #000;
        color: #888;
    }
    """

    BINDINGS = [
        ("q", "quit", "退出"),
        ("ctrl+c", "quit", "退出"),
    ]

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        yield Header()
        with TabbedContent(id="tabs", initial="funds"):
            with TabPane("📊 基金涨跌", id="funds"):
                yield DataTable(id="fund-table")
            with TabPane("📈 上涨行业", id="rise"):
                yield DataTable(id="rise-table")
            with TabPane("📉 下跌行业", id="fall"):
                yield DataTable(id="fall-table")
        yield Footer()

    def on_mount(self) -> None:
        """应用启动时初始化"""
        # 初始化基金表格
        fund_table = self.query_one("#fund-table", DataTable)
        fund_table.add_column("基金编号", width=10)
        fund_table.add_column("基金名称", width=50)
        fund_table.add_column("实时涨跌幅", width=15)
        fund_table.zebra_stripes = True

        # 初始化上涨行业表格
        rise_table = self.query_one("#rise-table", DataTable)
        rise_table.add_column("排名", width=6)
        rise_table.add_column("行业名称", width=30)
        rise_table.add_column("主力净流入(亿)", width=15)
        rise_table.zebra_stripes = True

        # 初始化下跌行业表格
        fall_table = self.query_one("#fall-table", DataTable)
        fall_table.add_column("排名", width=6)
        fall_table.add_column("行业名称", width=30)
        fall_table.add_column("主力净流入(亿)", width=15)
        fall_table.zebra_stripes = True

        # 首次加载数据
        self.refresh_data()
        
        # 启动定时刷新
        self.set_interval(refresh_interval, self.refresh_data)

    @work(thread=True)
    def refresh_data(self) -> None:
        """刷新所有数据 - 在后台线程中运行"""
        try:
            # 获取基金数据
            fund_data = {}
            for fund_code in fund_codes:
                try:
                    fund_data[fund_code] = get_gszzl(fund_code, retry)
                except Exception as e:
                    self.log.error(f"获取基金 {fund_code} 数据失败: {e}")
                    fund_data[fund_code] = None
            self.log(f"debug {fund_data}")
            # 获取行业数据
            industry_data = get_industry(retry)
            # 使用 call_from_thread 安全地更新 UI
            self.call_from_thread(self._update_ui, fund_data, industry_data)

        except Exception as e:
            self.log.error(f"刷新数据失败: {e}")
            self.log.error(traceback.format_exc())

    def _update_ui(self, fund_data: dict, industry_data: list) -> None:
        """更新 UI - 在主线程中运行"""
        # 更新标题
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.title = f"🚀 基金监控助手 (上次刷新: {now})"

        # 更新基金表格
        fund_table = self.query_one("#fund-table", DataTable)
        fund_table.clear()

        sorted_items = sorted(
            fund_data.items(),
            key=lambda x: float(x[1]["gszzl"]) if x[1] is not None else -999,
            reverse=True,
        )

        for fund_code, fund_info in sorted_items:
            if fund_info is not None:
                fund_name = fund_info["name"]
                gszzl = float(fund_info["gszzl"])

                if gszzl > 0:
                    gszzl_str = f"🔴 +{gszzl:.2f}%"
                elif gszzl < 0:
                    gszzl_str = f"🟢 {gszzl:.2f}%"
                else:
                    gszzl_str = "⚪ 0.00%"

                fund_table.add_row(fund_code, fund_name, gszzl_str)
            else:
                fund_table.add_row(fund_code, "数据获取失败", "--")

        # 更新上涨行业表格
        rise_table = self.query_one("#rise-table", DataTable)
        rise_table.clear()

        rise_data = [item for item in industry_data if item.get("f62", 0) > 0]
        rise_data.sort(key=lambda x: x.get("f62", 0), reverse=True)

        for idx, item in enumerate(rise_data[:top_k], 1):
            industry_name = item.get("f14", "未知")
            f62 = item.get("f62", 0) / 100000000
            rise_table.add_row(str(idx), industry_name, f"🔴 +{f62:.2f}")

        # 更新下跌行业表格
        fall_table = self.query_one("#fall-table", DataTable)
        fall_table.clear()

        fall_data = [item for item in industry_data if item.get("f62", 0) < 0]
        fall_data.sort(key=lambda x: x.get("f62", 0))

        for idx, item in enumerate(fall_data[:top_k], 1):
            industry_name = item.get("f14", "未知")
            f62 = item.get("f62", 0) / 100000000
            fall_table.add_row(str(idx), industry_name, f"🟢 {f62:.2f}")


if __name__ == "__main__":
    app = FundApp()
    app.run()

"""把圖標總表裁成獨立圖標並去背。

總表裁完會被刪除，所以重跑時已處理過的會自動略過。
"""
from pathlib import Path
from PIL import Image

IMG = Path(__file__).parent / "images"

# 總表檔名 -> 由左至右的圖標名稱
SHEETS = {
    # 第一批（研習簡報 v1）
    "icon_pids":    ["icon_digital", "icon_interact", "icon_visual"],
    "icon_agent":   ["icon_read", "icon_code", "icon_web", "icon_output"],
    "icon_redline": ["icon_rl1", "icon_rl2", "icon_rl3", "icon_rl4"],
    # 第二批（v2 修訂）
    "icon_route":   ["icon_hw", "icon_mind", "icon_page", "icon_game", "icon_exam"],
    "icon_tpack":   ["icon_tk", "icon_pk", "icon_ck"],
    "icon_samr":    ["icon_s", "icon_a", "icon_m", "icon_r"],
    "icon_lit":     ["icon_lit1", "icon_lit2", "icon_lit3", "icon_lit4"],
    "icon_vis":     ["icon_v1", "icon_v2", "icon_v3"],
    # 第三批（v3 修訂）
    "icon_flow4":   ["icon_say", "icon_write", "icon_git", "icon_live"],
    "icon_check2":  ["icon_detach", "icon_embed"],
}

DARK_THRESHOLD = 45
FADE_THRESHOLD = 80


def crop_sheet(sheet_name: str, names: list) -> None:
    src = IMG / f"{sheet_name}.png"
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    n = len(names)
    for i, name in enumerate(names):
        x0 = i * (w // n)
        x1 = (i + 1) * (w // n) if i < n - 1 else w
        col_w = x1 - x0
        sq = min(col_w, h)
        cx, cy = x0 + col_w // 2, h // 2
        crop = img.crop((cx - sq // 2, cy - sq // 2, cx + sq // 2, cy + sq // 2))
        crop = crop.resize((256, 256), Image.LANCZOS)
        crop.save(IMG / f"{name}.png")
        print(f"  裁切 {name}.png")


def remove_bg(path: Path) -> None:
    img = Image.open(path).convert("RGBA")
    data = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = data[x, y]
            lum = r * 0.299 + g * 0.587 + b * 0.114
            if lum < DARK_THRESHOLD:
                data[x, y] = (r, g, b, 0)
            elif lum < FADE_THRESHOLD:
                ratio = (lum - DARK_THRESHOLD) / (FADE_THRESHOLD - DARK_THRESHOLD)
                data[x, y] = (r, g, b, int(255 * ratio))
    img.save(path)


def main() -> None:
    produced = []
    for sheet, names in SHEETS.items():
        if not (IMG / f"{sheet}.png").exists():
            print(f"[{sheet}] 總表已處理過，略過")
            continue
        print(f"[{sheet}]")
        crop_sheet(sheet, names)
        produced.extend(names)

    if not produced:
        print("\n沒有需要處理的總表。")
        return

    print("\n去背中…")
    for name in produced:
        remove_bg(IMG / f"{name}.png")
        print(f"  去背 {name}.png")

    for sheet, names in SHEETS.items():
        p = IMG / f"{sheet}.png"
        if p.exists() and names[0] in produced:
            p.unlink()
            print(f"  移除總表 {sheet}.png")

    print(f"\n完成，共 {len(produced)} 個圖標。")


if __name__ == "__main__":
    main()

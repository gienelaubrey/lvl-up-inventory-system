from datetime import (
    date,
    datetime,
    time,
    timedelta,
    timezone,
)
from decimal import Decimal
from io import BytesIO
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.models.supplier import Supplier


MANILA_TIMEZONE = ZoneInfo("Asia/Manila")


def _date_range_to_utc(
    start_date: date,
    end_date: date,
):
    start_local = datetime.combine(
        start_date,
        time.min,
        tzinfo=MANILA_TIMEZONE,
    )

    end_local = datetime.combine(
        end_date + timedelta(days=1),
        time.min,
        tzinfo=MANILA_TIMEZONE,
    )

    return (
        start_local.astimezone(timezone.utc),
        end_local.astimezone(timezone.utc),
    )


def get_supplier_report_data(
    db: Session,
    supplier_id: int,
    start_date: date,
    end_date: date,
):
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )

    if not supplier:
        raise ValueError("Supplier not found")

    products = (
        db.query(Product)
        .filter(
            Product.supplier_id == supplier_id
        )
        .order_by(Product.sku.asc())
        .all()
    )

    start_utc, end_utc = (
        _date_range_to_utc(
            start_date,
            end_date,
        )
    )

    product_ids = [
        product.id
        for product in products
    ]

    if product_ids:
        movements = (
            db.query(StockMovement)
            .filter(
                StockMovement.product_id.in_(
                    product_ids
                ),
                StockMovement.created_at
                >= start_utc,
                StockMovement.created_at
                < end_utc,
            )
            .all()
        )
    else:
        movements = []

    stats = {}

    for product in products:
        stats[product.id] = {
            "sku": product.sku,
            "name": product.name,
            "stock_in": 0,
            "stock_out": 0,
            "units_sold": 0,
            "sales_value": Decimal("0"),
            "current_stock":
                product.current_stock,
            "selling_price":
                Decimal(product.selling_price),
        }

    for movement in movements:
        product = stats.get(
            movement.product_id
        )

        if not product:
            continue

        if movement.movement_type == "IN":
            product["stock_in"] += (
                movement.quantity
            )

        elif movement.movement_type == "OUT":
            product["stock_out"] += (
                movement.quantity
            )

            if (
                movement.reason or ""
            ).upper() == "SALE":
                product["units_sold"] += (
                    movement.quantity
                )

                product["sales_value"] += (
                    Decimal(
                        movement.quantity
                    )
                    * product[
                        "selling_price"
                    ]
                )

    product_stats = list(
        stats.values()
    )

    fast_moving = sorted(
        product_stats,
        key=lambda item:
            item["units_sold"],
        reverse=True,
    )[:5]

    slow_moving = sorted(
        product_stats,
        key=lambda item:
            item["units_sold"],
    )[:5]

    total_stock_in = sum(
        item["stock_in"]
        for item in product_stats
    )

    total_stock_out = sum(
        item["stock_out"]
        for item in product_stats
    )

    total_current_stock = sum(
        item["current_stock"]
        for item in product_stats
    )

    total_units_sold = sum(
        item["units_sold"]
        for item in product_stats
    )

    total_sales_value = sum(
        (
            item["sales_value"]
            for item in product_stats
        ),
        Decimal("0"),
    )

    return {
        "supplier": supplier,
        "start_date": start_date,
        "end_date": end_date,
        "products": product_stats,
        "fast_moving": fast_moving,
        "slow_moving": slow_moving,
        "total_stock_in":
            total_stock_in,
        "total_stock_out":
            total_stock_out,
        "total_current_stock":
            total_current_stock,
        "total_units_sold":
            total_units_sold,
        "total_sales_value":
            total_sales_value,
    }


def _money(value):
    return (
        f"PHP {Decimal(value):,.2f}"
    )


def build_supplier_report_pdf(
    report,
):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="LVL UP Supplier Report",
        author="LVL UP Enterprises OPC",
    )

    styles = getSampleStyleSheet()

    brand = colors.HexColor(
        "#64161B"
    )

    dark = colors.HexColor(
        "#241D1C"
    )

    muted = colors.HexColor(
        "#756A67"
    )

    border = colors.HexColor(
        "#DED5CF"
    )

    soft = colors.HexColor(
        "#F8F3EF"
    )

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        textColor=brand,
        alignment=TA_CENTER,
        spaceAfter=4 * mm,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=dark,
        alignment=TA_CENTER,
        spaceAfter=1 * mm,
    )

    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=11,
        textColor=muted,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=brand,
        spaceBefore=5 * mm,
        spaceAfter=3 * mm,
    )

    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontSize=7.5,
        leading=9,
        textColor=dark,
    )

    story = []

    supplier = report["supplier"]

    story.append(
        Paragraph(
            "LVL UP ENTERPRISES OPC",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "SUPPLIER PERFORMANCE AND INVENTORY REPORT",
            subtitle_style,
        )
    )

    story.append(
        Spacer(1, 3 * mm)
    )

    report_info = [
        [
            "Supplier",
            supplier.name,
            "Report Period",
            (
                f"{report['start_date']}"
                f" to "
                f"{report['end_date']}"
            ),
        ],
        [
            "Contact Person",
            supplier.contact_person
            or "-",
            "Generated",
            datetime.now(
                MANILA_TIMEZONE
            ).strftime(
                "%Y-%m-%d %I:%M %p"
            ),
        ],
    ]

    info_table = Table(
        report_info,
        colWidths=[
            29 * mm,
            55 * mm,
            29 * mm,
            55 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    soft,
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, -1),
                    soft,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    dark,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (2, 0),
                    (2, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    border,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(info_table)
    story.append(
        Spacer(1, 5 * mm)
    )

    story.append(
        Paragraph(
            "Summary",
            section_style,
        )
    )

    summary_data = [
        [
            "Stock In",
            "Stock Out",
            "Units Sold",
            "Current Stock",
            "Sales Value",
        ],
        [
            str(
                report[
                    "total_stock_in"
                ]
            ),
            str(
                report[
                    "total_stock_out"
                ]
            ),
            str(
                report[
                    "total_units_sold"
                ]
            ),
            str(
                report[
                    "total_current_stock"
                ]
            ),
            _money(
                report[
                    "total_sales_value"
                ]
            ),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            31 * mm,
            31 * mm,
            31 * mm,
            31 * mm,
            44 * mm,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    brand,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, 1),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    border,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(summary_table)

    def performance_table(
        title,
        rows,
    ):
        story.append(
            Paragraph(
                title,
                section_style,
            )
        )

        if not rows:
            story.append(
                Paragraph(
                    "No products available.",
                    meta_style,
                )
            )
            return

        data = [
            [
                "SKU",
                "Product",
                "Units Sold",
                "Sales Value",
            ]
        ]

        for item in rows:
            data.append(
                [
                    Paragraph(
                        item["sku"],
                        cell_style,
                    ),
                    Paragraph(
                        item["name"],
                        cell_style,
                    ),
                    str(
                        item[
                            "units_sold"
                        ]
                    ),
                    _money(
                        item[
                            "sales_value"
                        ]
                    ),
                ]
            )

        table = Table(
            data,
            repeatRows=1,
            colWidths=[
                28 * mm,
                76 * mm,
                28 * mm,
                38 * mm,
            ],
        )

        table.setStyle(
            _standard_table_style(
                brand,
                border,
                soft,
            )
        )

        story.append(table)

    performance_table(
        "Fast-Moving Products",
        report["fast_moving"],
    )

    performance_table(
        "Slow-Moving Products",
        report["slow_moving"],
    )

    story.append(
        Paragraph(
            "Inventory Movement and Stock Balance",
            section_style,
        )
    )

    movement_data = [
        [
            "SKU",
            "Product",
            "Stock In",
            "Stock Out",
            "Sales",
            "Current",
        ]
    ]

    for item in report["products"]:
        movement_data.append(
            [
                Paragraph(
                    item["sku"],
                    cell_style,
                ),
                Paragraph(
                    item["name"],
                    cell_style,
                ),
                str(
                    item["stock_in"]
                ),
                str(
                    item["stock_out"]
                ),
                str(
                    item["units_sold"]
                ),
                str(
                    item[
                        "current_stock"
                    ]
                ),
            ]
        )

    if len(movement_data) == 1:
        movement_data.append(
            [
                "-",
                "No products assigned",
                "0",
                "0",
                "0",
                "0",
            ]
        )

    movement_table = Table(
        movement_data,
        repeatRows=1,
        colWidths=[
            24 * mm,
            67 * mm,
            20 * mm,
            21 * mm,
            18 * mm,
            20 * mm,
        ],
    )

    movement_table.setStyle(
        _standard_table_style(
            brand,
            border,
            soft,
        )
    )

    story.append(movement_table)

    story.append(
        Spacer(1, 8 * mm)
    )

    story.append(
        Paragraph(
            (
                "Fast/slow-moving classifications "
                "are based on SALE stock-out "
                "transactions within the selected "
                "report period. Current stock "
                "reflects inventory at report "
                "generation time."
            ),
            meta_style,
        )
    )

    document.build(
        story,
        onFirstPage=_page_footer,
        onLaterPages=_page_footer,
    )

    buffer.seek(0)

    return buffer


def _standard_table_style(
    brand,
    border,
    soft,
):
    return TableStyle(
        [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                brand,
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.white,
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    soft,
                ],
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.35,
                border,
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7.5,
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),
            (
                "ALIGN",
                (2, 1),
                (-1, -1),
                "CENTER",
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
        ]
    )


def _page_footer(
    canvas,
    doc,
):
    canvas.saveState()

    canvas.setStrokeColor(
        colors.HexColor(
            "#DED5CF"
        )
    )

    canvas.line(
        14 * mm,
        10 * mm,
        196 * mm,
        10 * mm,
    )

    canvas.setFont(
        "Helvetica",
        7,
    )

    canvas.setFillColor(
        colors.HexColor(
            "#756A67"
        )
    )

    canvas.drawString(
        14 * mm,
        6 * mm,
        "LVL UP Enterprises OPC - Inventory System",
    )

    canvas.drawRightString(
        196 * mm,
        6 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()
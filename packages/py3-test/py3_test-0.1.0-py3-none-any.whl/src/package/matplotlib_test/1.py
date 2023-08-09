import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

plt.figure(figsize=(10, 10))

ax = plt.gca()

data = [
    ["receive_product_sales_nums", 0, 40756],
    ["flink_datasc_app_first_consume_date", 0, 4005],
    ["receive_index_export_nums", 0, 3772],
    ["receive_history_order", 0, 3206],
    ["flink_datasc_applet_first_consume_date", 0, 1558],
    ["receive_decrease_add_nums", 0, 1124],
    ["receive_app_board_nums", 0, 1060],
    ["flink_datasc_cancel_order", 0, 649],
    ["receive_user_add_nums", 0, 591],
    ["receive_activity_sales_nums", 0, 535],
    ["receive_dmall_store_stockinventory_order", 0, 511],
    ["flink_datasc_submit_order", 0, 488],
    ["receive_dmall_store_recive_order", 0, 460],
    ["flink_datasc_pay_order_detail", 0, 288],
    ["receive_gq_sx_t_im_flow_inc_topic", 0, 264],
    ["receive_user_visit_nums", 0, 157],
    ["receive_decrease_visit_nums", 0, 157],
    ["receive_card_export_nums", 0, 157],
    ["receive_goods_list", 0, 113],
    ["receive_coupon_data_nums", 0, 111],
    ["flink_datasc_apply_return", 0, 74],
    ["receive_dmall_store_stockadjustment_order", 0, 63],
    ["receive_dmall_store_stockallocation_order", 0, 23],
    ["receive_dmall_store_stockconvert_order", 0, 19],
    ["receive_order_submit_nums", 0, 17],
    ["receive_datasc_liontry", 0, 16],
    ["receive_dmall_store_stockcollect_order", 0, 14],
    ["receive_eletron_stock_detail", 0, 9],
    ["receive_dmall_store_stockmove_order", 0, 6],
    ["receive_dmall_store_delivery_order", 0, 5],
    ["flink_datasc_pay_order", 0, 0],
    ["receive_gqw_goods_store", 0, 0],
    ["receive_inventory_iquidation", 0, 0],
    ["receive_inventory_iquidation", 0, 0],
    ["receive_inventory_iquidation", 0, 0],
]
column_labels = ["表名", "昨日新增", "总数量"]
ax.axis("tight")
ax.axis("off")
# 设置坐标标签字体大小
tb = ax.table(cellText=data, colLabels=column_labels, loc="center")
tb.auto_set_font_size(False)
tb.set_fontsize(10)
# tb.scale(1.5, 1.5)

tb[0, 0].set_facecolor("#363636")
tb[0, 1].set_facecolor("#363636")
tb[0, 2].set_facecolor("#363636")
tb[0, 0].set_text_props(color="w")
tb[0, 1].set_text_props(color="w")
tb[0, 2].set_text_props(color="w")

for _pos, cell in tb.get_celld().items():
    cell.set_height(0.03)

plt.tight_layout()
plt.show()
# plt.savefig(fname="a.png",figsize=[10,10])

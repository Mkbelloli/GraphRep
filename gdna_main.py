import xlrd
from GraphStorage.GraphPool import EntityGraphPool

ANCHOR_COLUMN = 3
MAX_COLUMN_RANGE = 100
MAX_ROW_RANGE = 100
def corep_loader_by_xls(filename):
    xl_workbook = xlrd.open_workbook(filename)
    sheet_names = xl_workbook.sheet_names()
    print('Sheet Names', sheet_names)

    for sheet_name in sheet_names:

        if sheet_name == "TOC": continue

        sheet = xl_workbook.sheet_by_name(sheet_name)
        if sheet.ncols < ANCHOR_COLUMN: continue

        print(sheet_name)
        # find the COLUMN_ANCHOR. This is the most left cell of column indexes:
        rowColAnchor = -1
        for i in range(0, sheet.nrows):
            if sheet.cell_value(i, ANCHOR_COLUMN).strip("'").isnumeric():
                rowColAnchor = i
                break

        # get column array
        column_array = []
        for i in range(ANCHOR_COLUMN, ANCHOR_COLUMN + MAX_COLUMN_RANGE):
            if i >= sheet.ncols:
                break
            if sheet.cell_value(rowColAnchor, i).strip("'").isnumeric():
                column_array.append((rowColAnchor, i, sheet.cell_value(rowColAnchor, i).strip("'")))

        row_array = []
        for i in range(rowColAnchor, rowColAnchor + MAX_ROW_RANGE):
            if i >= sheet.nrows:
                break

            if sheet.cell_value(i, ANCHOR_COLUMN-1).strip("'").isnumeric():
                row_array.append((i, ANCHOR_COLUMN-1, sheet.cell_value(i, ANCHOR_COLUMN-1).strip("'")))

        for c in column_array:
            for r in row_array:
                v = sheet.cell_value(r[0], c[1])
                for s in "€£$%# ":
                    v = v.replace(s, '')
                v = v.strip()
                if len(v)>0:
                    print("{} {} {} {}".format(sheet_name, r[2], c[2], v))


def corep_loader_by_xls2(filename):
    xl_workbook = xlrd.open_workbook(filename)
    sheet = xl_workbook.sheet_by_index(0)

    # get index by column
    titles = []
    for i in range(sheet.ncols):
        t = sheet.cell_value(0, i)
        titles.append( (t, i) )

    for i in range(1, sheet.nrows):
        for t, tind in titles:
            v = str(sheet.cell_value(i, tind))
            if len(v.strip()) >0:
                print("{}:{}".format(t, v))


if __name__ == "__main__":
    print("It's time to go!")

    #corep_loader_by_xls("COREP_2.8.xlsx")
    #corep_loader_by_xls2("C0100Sample.xlsx")
    from Loaders.CustomLoaders import RowXLSLoader

    x = RowXLSLoader("C0100Sample.xlsx")
    x.initialize()
    gs = EntityGraphPool()
    gs.print()
    print(gs.g_pool)
    rep_period = None
    for row in x:
        graph = gs.pop_graph(row["ENTITY_ID"])
        rep_period = row["REPORTED_PERIOD"]
        tid = row["TID_RECEIVED_MODULES"]
        for p, v in row.items():
            if p not in ["TID_RECEIVED_MODULES", "REPORTED_PERIOD", "ENTITY_ID", "MODULE_ID"]:
                graph.update_dp(rep_period, tid, p, v)
        gs.push_graph(row["ENTITY_ID"], graph)

    gs.check_graphs(rep_period)

    #gs.print()
    # gs.save()


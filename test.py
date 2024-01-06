self.path_items[self.level] = self.catalogs.currentRow()
if self.level == 0:
    shift = 0
else:
    shift = 1
if self.catalogs.currentItem().text() == "...":
    self.level -= 1
    if self.level == 0:
        self.parent_name = ""
    else:
        self.parent_name = self.parent_items[self.catalogs.currentRow() - shift][1]
else:
    self.path_items[self.level] = self.catalogs.currentRow()
    self.level += 1
    self.parent_name = self.parent_items[self.catalogs.currentRow() - shift][0]
    if self.level == len(self.path_items):
        self.path_items.append(0)
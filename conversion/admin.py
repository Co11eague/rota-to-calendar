from django.contrib import admin

from conversion.models import UploadedTable, TableCell


class TableCellInline(admin.TabularInline):  # or admin.StackedInline
	model = TableCell
	extra = 0


class UploadedTableAdmin(admin.ModelAdmin):
	list_display = ('user', 'image',)
	inlines = [TableCellInline]  # Display cells in the table's admin


admin.site.register(UploadedTable, UploadedTableAdmin)
admin.site.register(TableCell)


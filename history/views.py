from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from conversion.models import UploadedTable, TableCell


@login_required
def index(request):
	tables = UploadedTable.objects.all()
	return render(request, 'history/index.html', {'tables': tables})


# Create your views here.
def view_cells(request, table_id):
    # Fetch the selected table
    table = get_object_or_404(UploadedTable, id=table_id)
    # Fetch all cells related to this table
    cells = TableCell.objects.filter(table=table)
    return render(request, 'history/view_cells.html', {'table': table, 'cells': cells})
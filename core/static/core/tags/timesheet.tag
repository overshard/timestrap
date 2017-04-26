<timesheet>
    <td if={ !edit }>
        <a class="text-primary" onclick={ goToEntries }><strong>{ name }</strong></a>
    </td>
    <td if={ edit }><input type="text" class="form-control form-control-sm" ref="name" value="{ name }" onkeypress="return event.keyCode != 13;">
    <td class="text-right">
        <a class="btn btn-primary btn-sm" onclick={ goToTasks }>Tasks</a>
        <a if={ !edit } class="btn btn-warning btn-sm" onclick={ editTimesheet }>
            <i class="fa fa-pencil-square-o" aria-hidden="true"></i>
        </a>
        <a if={ edit } class="btn btn-success btn-sm" onclick={ saveTimesheet }>
            <i class="fa fa-floppy-o" aria-hidden="true"></i>
        </a>
    </td>


    <script>
        var self = this;
        var edit = false;


        editTimesheet(e) {
            self.edit = true;
            self.update();
        }


        goToTasks(e) {
            document.location.href = tasksUrl + e.item.id;
        }


        goToEntries(e) {
            document.location.href = entriesUrl + e.item.id;
        }


        saveTimesheet(e) {
            e.preventDefault();
            self.name = self.refs.name.value;
            quickFetch(self.url, 'put', self).then(function(data) {
                self.name.value = '';
                self.edit = false;
                self.update();
            });
        }
    </script>
</timesheet>

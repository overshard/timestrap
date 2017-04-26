<timesheet>
    <td if={ !edit }>{ name }</td>
    <td if={ edit }><input type="text" class="form-control form-control-sm" ref="name" value="{ name }" onkeypress="return event.keyCode != 13;">
    <td class="text-right">
        <a if={ !edit } class="btn btn-warning btn-sm" onclick={ editTimesheet }>Edit</a>
        <a if={ edit } class="btn btn-success btn-sm" onclick={ saveTimesheet }>Save</a>
        <a class="btn btn-primary btn-sm" onclick={ goToTasks }>Tasks</a>
        <a class="btn btn-primary btn-sm" onclick={ goToEntries }>Entries</a>
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

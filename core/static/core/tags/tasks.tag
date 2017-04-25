<tasks>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
                data-url="{ previous }"
                if={ previous }
                onclick={ tasksPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
                data-url="{ next }"
                if={ next }
                onclick={ tasksPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

    <form onsubmit={ submitTask }>
        <table class="tasks-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Name</th>
                    <th>Timesheet</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-info">
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="name" placeholder="Name">
                    </td>
                    <td>
						<select class="timesheet-select" ref="timesheet">
							<option each={ timesheets } value={ url }>{ name }</option>
						</select>
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ tasks }>
                    <td>{ name }</td>
                    <td>{ timesheet_details.name }</td>
                    <td class="text-right">
                        <a class="btn btn-warning btn-sm" onclick={ editTask }>Edit</a>
                        <a class="btn btn-primary btn-sm" data-id="{ id }" onclick={ goToEntries }>Entries</a>
                    </td>
                </tr>
            </tbody>
        </table>
    </form>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var self = this;


        getTasks(url) {
            url = (typeof url !== 'undefined') ? url : tasksApiUrl;

            $('.loading, .tasks-table').toggleClass('d-none');

            let tasks = quickFetch(url);
            let timesheets = quickFetch(timesheetsApiUrl);

			Promise.all([tasks, timesheets]).then(function(e) {
                self.update({
                    tasks: e[0].results,
                    timesheets: e[1].results,
                    next: e[0].next,
                    previous: e[0].previous
                });

                $('.loading, .tasks-table').toggleClass('d-none');
				$('.timesheet-select').chosen();
			});
        }


        tasksPage(e) {
            self.getEntries(e.currentTarget.getAttribute('data-url'));
        }


        goToEntries(e) {
            document.location.href = entriesUrl + e.item.id;
        }


        submitTask(e) {
            e.preventDefault();
            let body = {
                name: self.refs.name.value,
                timesheet: self.refs.timesheet.value
            }
            quickFetch(tasksApiUrl, 'post', body).then(function(data) {
                self.refs.name.value = '';
                self.refs.timesheet.value = '';
                self.tasks.unshift(data);
                self.update();
            });
        }


        editTask(e) {
            let task = e.item;
            let tr = e.target.parentElement.parentElement;
            let td = $(tr).find('td');

            if ($(tr).hasClass('editing')) {
                task.name = $(td[0]).find('input').val();
                task.timesheet = $(td[1]).find('select').val();
                quickFetch(task.url, 'put', task).then(function(data) {
                    $(tr).removeClass('editing');
                    $(td[0]).html(data.name);
                    $(td[1]).html(data.timesheet_details.name);
                    $(td[2]).find('.btn-warning').html('Edit');
                });
            } else {
                $(tr).addClass('editing');
                $(td[0]).html('<input type="text" class="form-control form-control-sm" value="' + task.name + '" onkeypress="return event.keyCode != 13;">');

                $('.timesheet-select').chosen('destroy');
                $(td[1]).html($('.timesheet-select').parent().html());
                $(td[1]).find('.timesheet-select option[value="' + task.timesheet + '"]').attr('selected', 'selected');
                $('.timesheet-select').chosen();

                $(td[2]).find('.btn-warning').html('Save');
            }
        }


        self.getTasks();
    </script>
</tasks>

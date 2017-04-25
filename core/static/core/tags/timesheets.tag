<timesheets>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
                data-url="{ previous }"
                if={ previous }
                onclick={ timesheetsPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
                data-url="{ next }"
                if={ next }
                onclick={ timesheetsPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

    <form onsubmit={ submitTimesheet }>
        <table class="timesheets-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Name</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-info">
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="name" placeholder="Name">
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ timesheets }>
                    <td>{ name }</td>
                    <td class="text-right">
                        <a class="btn btn-warning btn-sm" onclick={ editTimesheet }>Edit</a>
                        <a class="btn btn-primary btn-sm" onclick={ goToTasks }>Tasks</a>
                        <a class="btn btn-primary btn-sm" onclick={ goToEntries }>Entries</a>
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

        getTimesheets(url) {
            url = (typeof url !== 'undefined') ? url : timesheetsApiUrl;

            $('.loading, .timesheets-table').toggleClass('d-none');

            autoFetch(url).then(function(data) {
                $('.loading, .timesheets-table').toggleClass('d-none');

                self.update({
                    timesheets: data.results,
                    next: data.next,
                    previous: data.previous
                });
            });
        }

        timesheetsPage(e) {
            self.getTimesheets(e.currentTarget.getAttribute('data-url'));
        }

        goToTasks(e) {
            document.location.href = tasksUrl + e.item.id;
        }

        goToEntries(e) {
            document.location.href = entriesUrl + e.item.id;
        }

        submitTimesheet(e) {
            e.preventDefault();
            let body = {
                name: self.refs.name.value
            }
            autoFetch(timesheetsApiUrl, 'post', body).then(function(data) {
                self.refs.name.value = '';
                self.getTimesheets();
            });
        }

        editTimesheet(e) {
            let timesheet = e.item;
            let tr = e.target.parentElement.parentElement;
            let td = $(tr).find('td');
            if ($(tr).hasClass('editing')) {
                timesheet.name = $(td[0]).find('input').val();
                autoFetch(timesheet.url, 'put', timesheet).then(function(data) {
                    $(tr).removeClass('editing');
                    $(td[0]).html(data.name);
                    $(td[1]).find('.btn-warning').html('Edit');
                });
            } else {
                $(tr).addClass('editing');
                $(td[1]).find('.btn-warning').html('Save');
                $(td[0]).html('<input type="text" class="form-control form-control-sm" value="' + timesheet.name + '">');
            }
        }

        self.getTimesheets();
    </script>
</timesheets>

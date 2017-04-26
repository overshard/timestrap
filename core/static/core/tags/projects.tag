<projects>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
                data-url="{ previous }"
                if={ previous }
                onclick={ projectsPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
                data-url="{ next }"
                if={ next }
                onclick={ projectsPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

    <form onsubmit={ submitProject }>
        <table class="projects-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Name</th>
                    <th>Client</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-info">
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="name" placeholder="Name">
                    </td>
                    <td>
						<select class="client-select" ref="client">
							<option each={ clients } value={ url }>{ name }</option>
						</select>
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ projects }>
                    <td>{ name }</td>
                    <td>{ client_details.name }</td>
                    <td class="text-right">
                        <a class="btn btn-warning btn-sm" onclick={ editProject }>Edit</a>
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


        getProjects(url) {
            url = (typeof url !== 'undefined') ? url : projectsApiUrl;

            $('.loading, .projects-table').toggleClass('d-none');

            let projects = quickFetch(url);
            let clients = quickFetch(clientsApiUrl);

			Promise.all([projects, clients]).then(function(e) {
                self.update({
                    projects: e[0].results,
                    clients: e[1].results,
                    next: e[0].next,
                    previous: e[0].previous
                });

                $('.loading, .projects-table').toggleClass('d-none');
				$('.client-select').chosen();
			});
        }


        projectsPage(e) {
            self.getEntries(e.currentTarget.getAttribute('data-url'));
        }


        goToEntries(e) {
            document.location.href = entriesUrl + e.item.id;
        }


        submitProject(e) {
            e.preventDefault();
            let body = {
                name: self.refs.name.value,
                client: self.refs.client.value
            }
            quickFetch(projectsApiUrl, 'post', body).then(function(data) {
                self.refs.name.value = '';
                self.refs.client.value = '';
                self.projects.unshift(data);
                self.update();
            });
        }


        editProject(e) {
            let project = e.item;
            let tr = e.target.parentElement.parentElement;
            let td = $(tr).find('td');

            if ($(tr).hasClass('editing')) {
                project.name = $(td[0]).find('input').val();
                project.client = $(td[1]).find('select').val();
                quickFetch(project.url, 'put', project).then(function(data) {
                    $(tr).removeClass('editing');
                    $(td[0]).html(data.name);
                    $(td[1]).html(data.client_details.name);
                    $(td[2]).find('.btn-warning').html('Edit');
                });
            } else {
                $(tr).addClass('editing');
                $(td[0]).html('<input type="text" class="form-control form-control-sm" value="' + project.name + '" onkeypress="return event.keyCode != 13;">');

                $('.client-select').chosen('destroy');
                $(td[1]).html($('.client-select').parent().html());
                $(td[1]).find('.client-select option[value="' + project.client + '"]').attr('selected', 'selected');
                $('.client-select').chosen();

                $(td[2]).find('.btn-warning').html('Save');
            }
        }


        self.getProjects();
    </script>
</projects>

<entry>
    <div class="col-sm-3">
        <div class="text-muted small">
            { project_details.client_details.name }
        </div>
        { project_details.name }
    </div>
    <div class="col-sm-5 d-flex align-self-end">
        { note }
    </div>
    <div class="col-sm-2 d-flex align-self-end">
        { duration }
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="entry-edit-menu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
        </button>
        <div class="dropdown-menu" aria-labelledby="entry-edit-menu">
            <a class="dropdown-item" href="#">Restart</a>
            <a class="dropdown-item" href="#">Edit</a>
            <a class="dropdown-item" href="#">Delete</a>
        </div>
    </div>


    <script>
        var self = this;
    </script>
</entry>

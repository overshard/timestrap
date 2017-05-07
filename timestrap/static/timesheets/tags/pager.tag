<pager>
    <button class="btn btn-primary btn-sm pull-right rounded-0"
            data-url={ this.parent.next }
            if={ this.parent.next }
            onclick={ loadDataUrl }>
        Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
    </button>

    <button class="btn btn-primary btn-sm pull-right mr-1 rounded-0"
            data-url={ this.parent.previous }
            if={ this.parent.previous }
            onclick={ loadDataUrl }>
        <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
    </button>


    <script>
        loadDataUrl(e) {
            this.opts.update(e.currentTarget.getAttribute('data-url'));
        }
    </script>
</pager>

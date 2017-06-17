<template>
<div class="container">
    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-3">
            Created
        </div>
        <div class="col-5">
            Client
        </div>
        <div class="col-2">
            Amount
        </div>
        <div class="col-2">
            Paid?
        </div>
    </div>

    <div class="entry-rows">
        <div class="entry row py-2 bg-faded small" v-for="invoice in invoices">
            <div class="col">
                {{ moment(invoice.created) }}
            </div>
            <div class="col">
                {{ invoice.client_details.name }}
            </div>
            <div class="col">
                $ {{ invoice.amount }}
            </div>
            <div class="col">
                {{ moment(invoice.paid) }}
            </div>
        </div>
    </div>
</div>
</template>


<script>
export default {
    data() {
        return {
            invoices: null
        };
    },
    methods: {
        getInvoices(url) {
            url = (typeof url !== 'undefined') ? url : timestrapConfig.API_URLS.INVOICES;

            let invoicesFetch = this.$quickFetch(url);

            invoicesFetch.then(data => {
                this.invoices = data;
            });
        },
        moment(date) {
            if (date) {
                return moment(date).format('LL');
            } else {
                return 'Not Paid';
            }
        }
    },
    mounted() {
        return this.getInvoices();
    },
};
</script>

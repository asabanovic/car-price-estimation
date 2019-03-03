Number.prototype.formatMoney = function(decPlaces, thouSeparator, decSeparator) {
    var n = this,
        decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
        decSeparator = decSeparator == undefined ? "." : decSeparator,
        thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
        sign = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "");
};

var app = new Vue({
    el: '#app',
    data: {

        data: {
            'brand' : null,
            'models': [],
            'fuel': null,
            'volume': null,
            'mileage': 0,
            'year': null,
            'model': null
        },

        prediction: null,

        loading: false,

        warning: null

    },
    watch: {

    },
//    delimiters: ['[[',']]'],

    methods: {
        getModels() {
			console.log("Getting organization images ...", this.data.brand);

            if (this.data.brand == null) {
                return false;
            }


            this.prediction = null;

			let data = {
				brand: this.data.brand
			};

			axios
				.post(
					'/models',
					data
				)
				.then(
					function(response) {
						console.log(response);
                        this.data.models = response.data;

                        this.$forceUpdate();
					}.bind(this)
				)
				.catch(function(error) {
					console.log(error);
				});
		},

		submit() {
		    console.log('Submitting');

            if (this.data.brand == null ||
                this.data.fuel == null ||
                this.data.volume == null ||
                this.data.year == null ||
                this.data.model == null
            ) {
                this.warning = 'Sva polja su obavezna, molimo Vas da ih popunite.'
                this.$forceUpdate();
                return false;
            }

            this.warning = null;

            this.loading = true;

			axios
				.post(
					'/predict',
					this.data
				)
				.then(
					function(response) {
						console.log(response);
                        this.prediction = response.data.formatMoney(0,',','.');
                        this.loading = false;
                        this.$forceUpdate();
					}.bind(this)
				)
				.catch(function(error) {
				    this.loading = false;
					console.log(error);
				});
		}
    },

    created() {

    }
});
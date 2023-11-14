Vue.component('v-select', VueSelect.VueSelect);

new Vue({
    el: '#app',
    data: {
        rotinas: {}, // Dados existentes
        campos: [
            "ROTINA", "EXEC_TS2", "EXEC_TS6", "EXEC_TS8", "EXEC_TT7", 
            "ULTIMO_PROCESSAMENTO", "ARQUIVO_TS2", "ARQUIVO_TS6", 
            "ARQUIVO_TS8", "ARQUIVO_TT7", "MOTOR", "E_S", "INCLUDE"
        ],
        activePage: 'home', // Dados existentes
        todasRotinas: [], // Nova propriedade para armazenar todas as rotinas
        rotinasSelecionadas: [] // Nova propriedade para armazenar as rotinas selecionadas
    },
    methods: {
        // Método existente para buscar rotinas
        fetchRotinas: function() {
            axios.post('/codes/rotinas', {
                rotinasSelecionadas: this.rotinasSelecionadas
            })
            .then(response => {
                this.rotinas = response.data;
            })
            .catch(error => {
                console.error("Houve um erro na requisição: ", error);
            });
        },
        // Novo método para definir a página ativa
        setActivePage: function(page) {
            this.activePage = page;
        },
        // Novo método para buscar a lista de todas as rotinas
        fetchTodasRotinas: function() {
            axios.post('/codes/listarotinas')
                .then(response => {
                    this.todasRotinas = response.data;
                })
                .catch(error => {
                    console.error("Erro ao buscar todas as rotinas: ", error);
                });
        }
    },
    mounted() {
        // Chama o novo método para buscar todas as rotinas quando o componente é montado
        this.fetchTodasRotinas();
    }
});

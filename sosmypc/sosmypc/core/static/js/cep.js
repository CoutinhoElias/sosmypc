$(document).ready(function() {

    function limpa_formulario_cep() {
        // Limpa valores do formulário de cep.
        $("#id_logradouro").val("");
        $("#id_bairro").val("");
        $("#id_cidade").val("");
        $("#id_estado").val("");
    }
    
    //Quando o campo cep perde o foco.
    $("#id_cep").blur(function() {

        //Nova variável "cep" somente com dígitos.
        var cep = $(this).val().replace(/\D/g, '');

        //Verifica se campo cep possui valor informado.
        if (cep != "") {

            //Expressão regular para validar o CEP.
            var validacep = /^[0-9]{8}$/;

            //Valida o formato do CEP.
            if(validacep.test(cep)) {

                //Preenche os campos com "..." enquanto consulta webservice.
                $("#id_logradouro").val("...")
                $("#id_bairro").val("...")
                $("#id_cidade").val("...")
                $("#id_estado").val("...")

                //Consulta o webservice viacep.com.br/
                $.getJSON("//viacep.com.br/ws/"+ cep +"/json/?callback=?", function(dados) {

                    if (!("erro" in dados)) {
                        //Atualiza os campos com os valores da consulta.
                        $("#id_logradouro").val(dados.logradouro);
                        $("#id_bairro").val(dados.bairro);
                        $("#id_cidade").val(dados.localidade);
                        $("#id_estado").val(dados.uf);

                        // Adiciona a classe 'active' aos campos já preenchidos, isto faz com que o
                        // 'label' do campo fique 'alto'
                        document.getElementById("id_bairro_container").childNodes[3].className="active";
                        document.getElementById("id_cidade_container").childNodes[3].className="active";
                        document.getElementById("id_estado_container").childNodes[3].className="active";
                    } //end if.
                    else {
                        //CEP pesquisado não foi encontrado.
                        limpa_formulario_cep();
                        alert("CEP não encontrado.");
                    }
                });
            } //end if.
            else {
                //cep é inválido.
                limpa_formulario_cep();
                alert("Formato de CEP inválido.");
            }
        } //end if.
        else {
            //cep sem valor, limpa formulário.
            limpa_formulario_cep();
        }
    });
});

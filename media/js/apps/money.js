/*
 * showGridLancamento
 * Exibe grid contendo os lancamentos cadastrados. No momento que a pagina
 * é carregada, exibde todos os lancamentos. Quando é escolhido algum filtro
 * então é criado um novo grid e inserido em outra aba do painel central.
 */
function showGridLancamento(params) {
    // id unico, string ou int
    var id = params['id'];
    
    // titulo do grid que vai aparecer na tela
    var title = params['title'];
    
    // url que retorna o conteudo a ser exibido no grid
    var datastoreUrl = params['datastoreUrl'];
    
    // id do grid formado por uma string + id do item clicado
    var datagridId = 'gridLancamento'+id;
    
    // Total de linhas exibidos no grid
    var LINHAS_POR_GRID = 31;
    
    /*
     * Se o data grid nao existe, entao cria um novo
     */ 
    if (! Ext.getCmp(datagridId)) {
        
        /*
         * Dados a serem exibidos no grid
         */ 
        var store = new Ext.data.Store({
            autoLoad: false,
            restful: true,
            reader: new Ext.data.JsonReader({
                totalProperty: 'total',
                root: 'rows',
                id: 'id',
                fields: [
                    { name: 'id' },
                    { name: 'vencimento', type: 'date', dateFormat: 'd/m/Y' },
                    { name: 'desc', },
                    { name: 'tipo', },
                    { name: 'pago', },
                    { name: 'valor' },
                    { name: 'saldo' }
                ]
            }),
            proxy: new Ext.data.HttpProxy({
                method: 'GET',
                url: datastoreUrl
            })
        });

        /*
         * Datagrid contendo os lancamentos cadastrados
         * 
         * Principais configuracoes:
         * 
         * 1. colModel:
         *    Cria as colunas do grid associadas aos indices do datastore.
         * 
         * 2. listeners:
         *    Acoes executadas de acordo com um evento do grid. Por exemplo,
         *    para um duplo clique sobre uma linha, o evento é rowdblclick.
         * 
         * 3. bbar:
         *    Bottom bar - barra de ferramenta inferior. Muita usada para
         *    exibir controles de navegação e paginação.
         * 
         * 4. tbar:
         *    Top bar - barra de ferramenta superior. Contém os botões 
         *    novo, editar e deletar.
         */
        var grid = new Ext.grid.GridPanel({
            id: ''+id,
            frame: false,
            border: true,
            title: 'Lançamentos '+title,
            autoExpandColumn: 'desc',
            stripeRows: true,
            store: store,
            colModel: new Ext.grid.ColumnModel({
                // Valores padroes para as colunas
                defaults: {
                    width: 100,
                    sortable: false,
                    menuDisabled: true,
                    autoWidth: true,
                },
                columns: [
                    //new Ext.grid.RowNumberer(),
                    {
                        header: 'ID',
                        hidden: true
                    }, {
                        header: 'Data',
                        dataIndex: 'vencimento',
                        renderer: Ext.util.Format.dateRenderer('d/m/Y'),
                        sortable: true
                    }, {
                        header: 'Descrição',
                        dataIndex: 'desc',
                        id: 'desc',
                    }, {
                        header: 'Pago',
                        dataIndex: 'pago',
                    }, {
                        header: 'Valor',
                        dataIndex: 'valor',
                    }, {
                        header: 'Saldo',
                        dataIndex: 'saldo',
                    }
                ],
            }),
            listeners: {
                /*
                 * Acao a ser realizada quando houver um clique duplo na linha
                 */ 
                rowdblclick: {
                    fn: function(g, i, e) {
                        var p, title, id;
                        id = g.getSelectionModel().getSelected().get('id');
                        if (id > 0) {
                            //title = g.getSelectionModel().getSelected().get('name');
                            editLancamento(id);
                        } else
                            Ext.Msg.alert('Erro', 'Nenhum item selecionado.');
                    }
                }
            },
            sm: new Ext.grid.RowSelectionModel({
                singleSelect: true,
            }),
            bbar: new Ext.PagingToolbar({
                pageSize: LINHAS_POR_GRID,
                store: store,
                displayInfo: true,
                beforePageText: 'Página ',
                afterPageText: ' de {0}',
                displayMsg: 'Exibindo {0} - {1} de {2}',
                emptyMsg: "Nenhum resultado",
            }),
            tbar: [{
                text: 'Novo',
                iconCls: 'new-icon',
                cls:'x-btn-text-icon',
                handler: function() {
                    novoLancamento();
                }
            }, {
                text: 'Editar',
                iconCls: 'edit-icon',
                cls:'x-btn-text-icon',
                handler: function() {
                    var id = grid.getSelectionModel().getSelected().get('id');
                    if (id > 0)
                        editLancamento(id);
                }
            }, {
                text: 'Apagar',
                iconCls: 'eraser-icon',
                cls:'x-btn-text-icon',
                handler: function() {
                var id = grid.getSelectionModel().getSelected().get('id');
                if (id > 0)
                    Ext.Msg.confirm('Confirmação', 'Tem certeza?', function(btn, text) {
                        if (btn == 'yes') {
                            url = URL_MONEY_DEL.replace('/0','/'+id);
                            Ext.Ajax.request({
                                url: url,
                                method: 'DELETE',
                                success: function() { grid.getStore().reload() },
                                failure: function() { Ext.Msg.alert('Erro','Erro ao tentar excluir item com ID '+id); }
                            });
                        }
                    });
                
                }
            }]
        });
      
        /*
         * Executa o datastore. O store consulta uma url e obtem os dados
         * a serem exibidos no grid.
         */
        store.load({params:{start: 0, limit: LINHAS_POR_GRID}});
      
        /*
         * Adiciona o grid na tela principal, especificamente na viewport
         * center cujo id é tbMain. Cada grid criado vai para uma aba diferente.
         */
        Ext.getCmp('tbMain').add(grid).show();
    
    } else
        // Se o grid está sendo exibido, então coloca o foco nele
        Ext.getCmp('tbMain').activate('gridLancamento');

}

function _Form(params) {
    var id = params['id'];
    if (! Ext.getCmp('form'+id)) {
        var form = new Ext.FormPanel({
            id: 'form'+id,
            labelWidth: 100,
            url: params['urlForm'],
            method: params['method'],
            autoScroll: true,
            height: 140,
            frame: false,
            border: false,
            bodyStyle : 'padding:10px;',
            defaults: { anchor: '95%' },
            defaultType: 'textfield',
            buttons: [{
                text: 'Salvar',
                handler: function() {
                    if (form.getForm().isValid())
                        form.getForm().submit({
                            success: function(f,a) {
                                //Ext.Msg.alert('Alert', 'Sucesso.');
                                form.getForm().reset();
                                Ext.getCmp('winLancamento').close();
                            },
                            failure: function(f,a){
                                Ext.Msg.alert('Error', 'Erro ao cadastrar.<br>Verifique se os campos foram preenchidos corretamente.');
                            }
                        });
                    else
                        Ext.Msg.alert('Error', 'Preencha corretamente o formul&aacute;rio.');
                }
            }]
        });
    
        Ext.Ajax.request({
            url: params['urlAjax'],
            success: function(r) {
                var j = Ext.decode(r.responseText);
                if (j.status == 'error')
                    Ext.Msg.alert('Error',j.msg);
                else {
                    Ext.each(j, function(data) {
                        form.add(data);
                    });
                    form.doLayout();
                }
            }
        });
        
        return form;
    }
}

function _openWin(form) {
    if (! Ext.getCmp('winLancamento'))
        var win = new Ext.Window({
            id: 'winLancamento',
            title: 'Lançamento',
            width: 450,
            height: 325,
            layout: 'fit',
            items: [ form, ],
            listeners: {
                close: function() { Ext.getCmp('gridLancamento').getStore().reload(); }
            }
        }).show();
}

function novoLancamento() {
    var form = _Form({id: 'formNovoLancamento', urlForm: URL_MONEY_ADD, urlAjax: URL_MONEY_NEW, method: 'POST'});
    _openWin(form);
    //$('.brdatefield').setMask('99/99/9999');
}

function editLancamento(id) {
    var form = _Form({id: 'formEditLancamento', urlForm: URL_MONEY_UPD.replace('/0','/'+id) , urlAjax: URL_MONEY_EDIT+'?id='+id, method: 'PUT'});
    _openWin(form);
}


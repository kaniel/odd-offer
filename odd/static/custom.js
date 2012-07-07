$(function(){

    $('.dropdown.auto-down').hover(function(){
        $(this).addClass('open');
    },function(){
        $(this).removeClass('open');
    })

    $.each($('.tip-search'), function(i,v){
        search_init(v, [], 10, '/search/tips')
    })

    $.each($('.tag-search'), function(i,v){
        tag_search(v, [], false)
    })

    /*** editable ***/

    $('.editable').hover(function(){
        $('.edit', this).fadeIn('fast');
    },function(){
        $('.edit', this).fadeOut('fast');
    });

    $('.editable .edit').click(function(){
        var editable = $(this).parents('.editable')
        var edited = editable.find('.edited');
        var edit_form = editable.find('.edit-form')
        var edited_item = edited.find('.edited-item');
        var edit_item = edit_form.find('.edit-item');
        var edit_cancel = edit_form.find('.edit-cancel');

        edited.hide('fast');
        edit_form.show('fast');
        edit_item.val(edited_item.text())
    });
    
    $('.editable .edit-cancel').click(function(){
        var editable = $(this).parents('.editable')
        var edited = editable.find('.edited');
        var edit_form = editable.find('.edit-form')

        edit_form.hide('fast');
        edited.show('fast');
    })

    $('.edit-form').ajaxForm({
        error: fail,
        success: success
    });

    $('.ajax-form').ajaxForm({
        error: fail,
        success: success
    });

    $('.tag-box').hover(function(){
        $('.only-follow', this).removeClass('hide');
    },function(){
        $('.only-follow', this).addClass('hide');
    })

    $('.only-follow').click(function(){
        self = $(this);
        $.ajax({
            url: "/follow/tag/follow",
            type: 'post',
            data: {tag:self.attr('data-tag')},
            success: function(data){
                if(data.errno != 'SUCCESS') return;
                self.siblings('.has-follow').removeClass('hide');
                self.remove();
            }
        });
    });
    
    $('.follow').click(function(){
        self = $(this);
        $.ajax({
            url: "/follow/tag/follow",
            type: 'post',
            data: {tag:self.attr('data-tag')},
            success: function(data){
                if(data.errno != 'SUCCESS') return;
                self.siblings('.unfollow').removeClass('hide');
                self.addClass('hide');
            }
        });
    });


    $('.unfollow').click(function(){
        self = $(this);
        $.ajax({
            url: "/follow/tag/unfollow",
            type: 'post',
            data: {tag:self.attr('data-tag')},
            success: function(data){
                if(data.errno != 'SUCCESS') return;
                self.siblings('.follow').removeClass('hide');
                self.addClass('hide');
            }
        });
    });


});

function search_init(ele, source, max, url){
    var cache = {};

    var typeahead = $(ele).typeahead({
        source: source,
        items : max,
        getter: function(item){
            return item[0]
        },
        lookup: function(event){
            var query = $(ele).val()
            if(query){
                if(cache[query] != null){
                    typeahead.source = cache[query]
                }else{
                    $.getJSON(url, {query:query}, function(data){
                        typeahead.source = tip_format(data)
                        cache[query] = typeahead.source
                        typeahead._lookup(event)
                    })
                }
            }
            return typeahead._lookup(event)
        },
        sorter: function(items){
            items = typeahead._sorter(items)
            return classify(items, max, typeahead.query.toLowerCase())
        },
        highlighter: function(item){
            hl = typeahead._highlighter(item)
            return item[1].replace(new RegExp('&&','g'), hl)
        },
        onSelect: function(val){
            location.href = val[3]
        },
    }).data('typeahead')

    return this;
}

function tip_format(data){
    var tips = []

    $.each(data.tags,function(i,tag){
        tips.push([tag.tag, '<img src="/static/'+tag.photo+'" /> &&', 'tag', '/tag/'+tag.tag]);  
    });

    $.each(data.questions,function(i,que){
        tips.push([que.title, '<img src="/static/img/question.png" /> &&', 'question', '/question/'+que.id]);
    });

    $.each(data.resources,function(i,res){
        tips.push([res.title, '<img src="/static/img/resource.png" /> &&', 'resource', '/resource/'+res.id]);  
    });

    return tips;
}

function classify(items, max, query){
    var tags = []
        , questions = []
        , resources = [];

    $.each(items, function(k, v){
        switch(v[2]){
        case 'tag':
            tags.push(v);
            break;
        case 'question':
            questions.push(v);
            break;
        case 'resource':
            resources.push(v);
            break;
        }
    });

    sum = tags.length + questions.length + resources.length;

    if(sum){
        tags = tags.slice(0, tags.length / sum * max);
        questions = questions.slice(0, questions.length / sum * max);
        resources = resources.slice(0, resources.length / sum * max);
    }

    pres = [['','搜索 '+query,'','/search/?query='+query]]

    return pres.concat(tags, questions, resources);
}

function trim(str){
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

function fail(msg){
    if(typeof(msg) != 'string') msg = '您的操作没有成功' 
    alert(msg)
}

function success(data){
    if(data.errno == 'SUCCESS' || data.status == 'OK'){
        window.location.reload(true)
    }else{
        fail(data.msg)
    }
}

function tag_format(data){
    var tags = []
    $.each(data.tags,function(i,t){
        tags.push([t.tag, t.tag, null, '<img src="/static/'+t.photo+'" />'+t.tag]);
    });
    return tags;
}

function textbox(_options) {
    var options = $.extend({
        element: '',
        url: '',
        format: function(data){return data;},
        placeholder: '',
        init_values: [],
        empty_submit: false,
        on_empty: null,
        on_bitBoxAdd: null,
        focus: false,
        on_selected: null,
        on_new: null,
        post_result: null,
    }, _options);

    var t = new $.TextboxList(options.element, {unique: true, plugins: {
        autocomplete: {method:'custom', placeholder:options.placeholder, on_selected:options.on_selected, on_new:options.on_new, post_result:options.post_result}}});

    $.each(options.init_values, function(i,v){
        t.add(v[0], v[1]);
    });
   
    if(options.empty_submit){
        t.addEvent('empty', function(){
            $(options.element).parent('.edit-form').submit();
        });
    }

    if(options.on_empty){
        t.addEvent('empty', options.on_empty);
    }
    
    if(options.on_bitBoxAdd){
        t.addEvent('bitBoxAdd', options.on_bitBoxAdd);
    }

    t.getContainer().addClass('textboxlist-loading');  
    $.getJSON(options.url, function(data){
        t.plugins['autocomplete'].setValues(options.format(data));
        t.getContainer().removeClass('textboxlist-loading');
        if(options.focus){
            $('input',t.getContainer()).focus();
        }
    }); 

    return t;
}

function tag_search(input, tags, empty_submit){
    var t = textbox({
        element: input,
        init_values: tags,
        empty_submit: empty_submit,
        placeholder: '搜索：标签',
        url: "/tag/obj",
        format: tag_format
    });

    return t;
}

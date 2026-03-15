// Unobtrusive Ajax support library for jQuery
// Copyright (c) .NET Foundation. All rights reserved.
// Licensed under the Apache License, Version 2.0. See License.txt in the project root for license information.
// @version v3.2.6
// 
// Microsoft grants you the right to use these script files for the sole
// purpose of either: (i) interacting through your browser with the Microsoft
// website or online service, subject to the applicable licensing or use
// terms; or (ii) using the files as included with a Microsoft product subject
// to that product's license terms. Microsoft reserves all other rights to the
// files not expressly granted by Microsoft, whether by implication, estoppel
// or otherwise. Insofar as a script file is dual licensed under GPL,
// Microsoft neither took the code under GPL nor distributes it thereunder but
// under the terms set out in this paragraph. All notices and licenses
// below are for informational purposes only.
!function(t){function a(t,a){for(var e=window,r=(t||"").split(".");e&&r.length;)e=e[r.shift()];return"function"==typeof e?e:(a.push(t),Function.constructor.apply(null,a))}function e(t){return"GET"===t||"POST"===t}function r(t,a){e(a)||t.setRequestHeader("X-HTTP-Method-Override",a)}function n(a,e,r){var n;r.indexOf("application/x-javascript")===-1&&(n=(a.getAttribute("data-ajax-mode")||"").toUpperCase(),t(a.getAttribute("data-ajax-update")).each(function(a,r){switch(n){case"BEFORE":t(r).prepend(e);break;case"AFTER":t(r).append(e);break;case"REPLACE-WITH":t(r).replaceWith(e);break;default:t(r).html(e)}}))}function i(i,u){var o,c,d,s;if(o=i.getAttribute("data-ajax-confirm"),!o||window.confirm(o)){c=t(i.getAttribute("data-ajax-loading")),s=parseInt(i.getAttribute("data-ajax-loading-duration"),10)||0,t.extend(u,{type:i.getAttribute("data-ajax-method")||void 0,url:i.getAttribute("data-ajax-url")||void 0,cache:"true"===(i.getAttribute("data-ajax-cache")||"").toLowerCase(),beforeSend:function(t){var e;return r(t,d),e=a(i.getAttribute("data-ajax-begin"),["xhr"]).apply(i,arguments),e!==!1&&c.show(s),e},complete:function(){c.hide(s),a(i.getAttribute("data-ajax-complete"),["xhr","status"]).apply(i,arguments)},success:function(t,e,r){n(i,t,r.getResponseHeader("Content-Type")||"text/html"),a(i.getAttribute("data-ajax-success"),["data","status","xhr"]).apply(i,arguments)},error:function(){a(i.getAttribute("data-ajax-failure"),["xhr","status","error"]).apply(i,arguments)}}),u.data.push({name:"X-Requested-With",value:"XMLHttpRequest"}),d=u.type.toUpperCase(),e(d)||(u.type="POST",u.data.push({name:"X-HTTP-Method-Override",value:d}));var p=t(i);if(p.is("form")&&"multipart/form-data"==p.attr("enctype")){var f=new FormData;t.each(u.data,function(t,a){f.append(a.name,a.value)}),t("input[type=file]",p).each(function(){var a=this;t.each(a.files,function(t,e){f.append(a.name,e)})}),t.extend(u,{processData:!1,contentType:!1,data:f})}t.ajax(u)}}function u(a){var e=t(a).data(d);return!e||!e.validate||e.validate()}var o="unobtrusiveAjaxClick",c="unobtrusiveAjaxClickTarget",d="unobtrusiveValidation";t(document).on("click","a[data-ajax=true]",function(t){t.preventDefault(),i(this,{url:this.href,type:"GET",data:[]})}),t(document).on("click","form[data-ajax=true] input[type=image]",function(a){var e=a.target.name,r=t(a.target),n=t(r.parents("form")[0]),i=r.offset();n.data(o,[{name:e+".x",value:Math.round(a.pageX-i.left)},{name:e+".y",value:Math.round(a.pageY-i.top)}]),setTimeout(function(){n.removeData(o)},0)}),t(document).on("click","form[data-ajax=true] :submit",function(a){var e=a.currentTarget.name,r=t(a.target),n=t(r.parents("form")[0]);n.data(o,e?[{name:e,value:a.currentTarget.value}]:[]),n.data(c,r),setTimeout(function(){n.removeData(o),n.removeData(c)},0)}),t(document).on("submit","form[data-ajax=true]",function(a){var e=t(this).data(o)||[],r=t(this).data(c),n=r&&(r.hasClass("cancel")||void 0!==r.attr("formnovalidate"));a.preventDefault(),(n||u(this))&&i(this,{url:this.action,type:this.method||"GET",data:e.concat(t(this).serializeArray())})})}(jQuery);;
/*! jQuery Validation Plugin - v1.19.5 - 7/1/2022
 * https://jqueryvalidation.org/
 * Copyright (c) 2022 Jörn Zaefferer; Licensed MIT */
!function(a){"function"==typeof define&&define.amd?define(["jquery"],a):"object"==typeof module&&module.exports?module.exports=a(require("jquery")):a(jQuery)}(function(a){a.extend(a.fn,{validate:function(b){if(!this.length)return void(b&&b.debug&&window.console&&console.warn("Nothing selected, can't validate, returning nothing."));var c=a.data(this[0],"validator");return c?c:(this.attr("novalidate","novalidate"),c=new a.validator(b,this[0]),a.data(this[0],"validator",c),c.settings.onsubmit&&(this.on("click.validate",":submit",function(b){c.submitButton=b.currentTarget,a(this).hasClass("cancel")&&(c.cancelSubmit=!0),void 0!==a(this).attr("formnovalidate")&&(c.cancelSubmit=!0)}),this.on("submit.validate",function(b){function d(){var d,e;return c.submitButton&&(c.settings.submitHandler||c.formSubmitted)&&(d=a("<input type='hidden'/>").attr("name",c.submitButton.name).val(a(c.submitButton).val()).appendTo(c.currentForm)),!(c.settings.submitHandler&&!c.settings.debug)||(e=c.settings.submitHandler.call(c,c.currentForm,b),d&&d.remove(),void 0!==e&&e)}return c.settings.debug&&b.preventDefault(),c.cancelSubmit?(c.cancelSubmit=!1,d()):c.form()?c.pendingRequest?(c.formSubmitted=!0,!1):d():(c.focusInvalid(),!1)})),c)},valid:function(){var b,c,d;return a(this[0]).is("form")?b=this.validate().form():(d=[],b=!0,c=a(this[0].form).validate(),this.each(function(){b=c.element(this)&&b,b||(d=d.concat(c.errorList))}),c.errorList=d),b},rules:function(b,c){var d,e,f,g,h,i,j=this[0],k="undefined"!=typeof this.attr("contenteditable")&&"false"!==this.attr("contenteditable");if(null!=j&&(!j.form&&k&&(j.form=this.closest("form")[0],j.name=this.attr("name")),null!=j.form)){if(b)switch(d=a.data(j.form,"validator").settings,e=d.rules,f=a.validator.staticRules(j),b){case"add":a.extend(f,a.validator.normalizeRule(c)),delete f.messages,e[j.name]=f,c.messages&&(d.messages[j.name]=a.extend(d.messages[j.name],c.messages));break;case"remove":return c?(i={},a.each(c.split(/\s/),function(a,b){i[b]=f[b],delete f[b]}),i):(delete e[j.name],f)}return g=a.validator.normalizeRules(a.extend({},a.validator.classRules(j),a.validator.attributeRules(j),a.validator.dataRules(j),a.validator.staticRules(j)),j),g.required&&(h=g.required,delete g.required,g=a.extend({required:h},g)),g.remote&&(h=g.remote,delete g.remote,g=a.extend(g,{remote:h})),g}}});var b=function(a){return a.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"")};a.extend(a.expr.pseudos||a.expr[":"],{blank:function(c){return!b(""+a(c).val())},filled:function(c){var d=a(c).val();return null!==d&&!!b(""+d)},unchecked:function(b){return!a(b).prop("checked")}}),a.validator=function(b,c){this.settings=a.extend(!0,{},a.validator.defaults,b),this.currentForm=c,this.init()},a.validator.format=function(b,c){return 1===arguments.length?function(){var c=a.makeArray(arguments);return c.unshift(b),a.validator.format.apply(this,c)}:void 0===c?b:(arguments.length>2&&c.constructor!==Array&&(c=a.makeArray(arguments).slice(1)),c.constructor!==Array&&(c=[c]),a.each(c,function(a,c){b=b.replace(new RegExp("\\{"+a+"\\}","g"),function(){return c})}),b)},a.extend(a.validator,{defaults:{messages:{},groups:{},rules:{},errorClass:"error",pendingClass:"pending",validClass:"valid",errorElement:"label",focusCleanup:!1,focusInvalid:!0,errorContainer:a([]),errorLabelContainer:a([]),onsubmit:!0,ignore:":hidden",ignoreTitle:!1,onfocusin:function(a){this.lastActive=a,this.settings.focusCleanup&&(this.settings.unhighlight&&this.settings.unhighlight.call(this,a,this.settings.errorClass,this.settings.validClass),this.hideThese(this.errorsFor(a)))},onfocusout:function(a){this.checkable(a)||!(a.name in this.submitted)&&this.optional(a)||this.element(a)},onkeyup:function(b,c){var d=[16,17,18,20,35,36,37,38,39,40,45,144,225];9===c.which&&""===this.elementValue(b)||a.inArray(c.keyCode,d)!==-1||(b.name in this.submitted||b.name in this.invalid)&&this.element(b)},onclick:function(a){a.name in this.submitted?this.element(a):a.parentNode.name in this.submitted&&this.element(a.parentNode)},highlight:function(b,c,d){"radio"===b.type?this.findByName(b.name).addClass(c).removeClass(d):a(b).addClass(c).removeClass(d)},unhighlight:function(b,c,d){"radio"===b.type?this.findByName(b.name).removeClass(c).addClass(d):a(b).removeClass(c).addClass(d)}},setDefaults:function(b){a.extend(a.validator.defaults,b)},messages:{required:"This field is required.",remote:"Please fix this field.",email:"Please enter a valid email address.",url:"Please enter a valid URL.",date:"Please enter a valid date.",dateISO:"Please enter a valid date (ISO).",number:"Please enter a valid number.",digits:"Please enter only digits.",equalTo:"Please enter the same value again.",maxlength:a.validator.format("Please enter no more than {0} characters."),minlength:a.validator.format("Please enter at least {0} characters."),rangelength:a.validator.format("Please enter a value between {0} and {1} characters long."),range:a.validator.format("Please enter a value between {0} and {1}."),max:a.validator.format("Please enter a value less than or equal to {0}."),min:a.validator.format("Please enter a value greater than or equal to {0}."),step:a.validator.format("Please enter a multiple of {0}.")},autoCreateRanges:!1,prototype:{init:function(){function b(b){var c="undefined"!=typeof a(this).attr("contenteditable")&&"false"!==a(this).attr("contenteditable");if(!this.form&&c&&(this.form=a(this).closest("form")[0],this.name=a(this).attr("name")),d===this.form){var e=a.data(this.form,"validator"),f="on"+b.type.replace(/^validate/,""),g=e.settings;g[f]&&!a(this).is(g.ignore)&&g[f].call(e,this,b)}}this.labelContainer=a(this.settings.errorLabelContainer),this.errorContext=this.labelContainer.length&&this.labelContainer||a(this.currentForm),this.containers=a(this.settings.errorContainer).add(this.settings.errorLabelContainer),this.submitted={},this.valueCache={},this.pendingRequest=0,this.pending={},this.invalid={},this.reset();var c,d=this.currentForm,e=this.groups={};a.each(this.settings.groups,function(b,c){"string"==typeof c&&(c=c.split(/\s/)),a.each(c,function(a,c){e[c]=b})}),c=this.settings.rules,a.each(c,function(b,d){c[b]=a.validator.normalizeRule(d)}),a(this.currentForm).on("focusin.validate focusout.validate keyup.validate",":text, [type='password'], [type='file'], select, textarea, [type='number'], [type='search'], [type='tel'], [type='url'], [type='email'], [type='datetime'], [type='date'], [type='month'], [type='week'], [type='time'], [type='datetime-local'], [type='range'], [type='color'], [type='radio'], [type='checkbox'], [contenteditable], [type='button']",b).on("click.validate","select, option, [type='radio'], [type='checkbox']",b),this.settings.invalidHandler&&a(this.currentForm).on("invalid-form.validate",this.settings.invalidHandler)},form:function(){return this.checkForm(),a.extend(this.submitted,this.errorMap),this.invalid=a.extend({},this.errorMap),this.valid()||a(this.currentForm).triggerHandler("invalid-form",[this]),this.showErrors(),this.valid()},checkForm:function(){this.prepareForm();for(var a=0,b=this.currentElements=this.elements();b[a];a++)this.check(b[a]);return this.valid()},element:function(b){var c,d,e=this.clean(b),f=this.validationTargetFor(e),g=this,h=!0;return void 0===f?delete this.invalid[e.name]:(this.prepareElement(f),this.currentElements=a(f),d=this.groups[f.name],d&&a.each(this.groups,function(a,b){b===d&&a!==f.name&&(e=g.validationTargetFor(g.clean(g.findByName(a))),e&&e.name in g.invalid&&(g.currentElements.push(e),h=g.check(e)&&h))}),c=this.check(f)!==!1,h=h&&c,c?this.invalid[f.name]=!1:this.invalid[f.name]=!0,this.numberOfInvalids()||(this.toHide=this.toHide.add(this.containers)),this.showErrors(),a(b).attr("aria-invalid",!c)),h},showErrors:function(b){if(b){var c=this;a.extend(this.errorMap,b),this.errorList=a.map(this.errorMap,function(a,b){return{message:a,element:c.findByName(b)[0]}}),this.successList=a.grep(this.successList,function(a){return!(a.name in b)})}this.settings.showErrors?this.settings.showErrors.call(this,this.errorMap,this.errorList):this.defaultShowErrors()},resetForm:function(){a.fn.resetForm&&a(this.currentForm).resetForm(),this.invalid={},this.submitted={},this.prepareForm(),this.hideErrors();var b=this.elements().removeData("previousValue").removeAttr("aria-invalid");this.resetElements(b)},resetElements:function(a){var b;if(this.settings.unhighlight)for(b=0;a[b];b++)this.settings.unhighlight.call(this,a[b],this.settings.errorClass,""),this.findByName(a[b].name).removeClass(this.settings.validClass);else a.removeClass(this.settings.errorClass).removeClass(this.settings.validClass)},numberOfInvalids:function(){return this.objectLength(this.invalid)},objectLength:function(a){var b,c=0;for(b in a)void 0!==a[b]&&null!==a[b]&&a[b]!==!1&&c++;return c},hideErrors:function(){this.hideThese(this.toHide)},hideThese:function(a){a.not(this.containers).text(""),this.addWrapper(a).hide()},valid:function(){return 0===this.size()},size:function(){return this.errorList.length},focusInvalid:function(){if(this.settings.focusInvalid)try{a(this.findLastActive()||this.errorList.length&&this.errorList[0].element||[]).filter(":visible").trigger("focus").trigger("focusin")}catch(b){}},findLastActive:function(){var b=this.lastActive;return b&&1===a.grep(this.errorList,function(a){return a.element.name===b.name}).length&&b},elements:function(){var b=this,c={};return a(this.currentForm).find("input, select, textarea, [contenteditable]").not(":submit, :reset, :image, :disabled").not(this.settings.ignore).filter(function(){var d=this.name||a(this).attr("name"),e="undefined"!=typeof a(this).attr("contenteditable")&&"false"!==a(this).attr("contenteditable");return!d&&b.settings.debug&&window.console&&console.error("%o has no name assigned",this),e&&(this.form=a(this).closest("form")[0],this.name=d),this.form===b.currentForm&&(!(d in c||!b.objectLength(a(this).rules()))&&(c[d]=!0,!0))})},clean:function(b){return a(b)[0]},errors:function(){var b=this.settings.errorClass.split(" ").join(".");return a(this.settings.errorElement+"."+b,this.errorContext)},resetInternals:function(){this.successList=[],this.errorList=[],this.errorMap={},this.toShow=a([]),this.toHide=a([])},reset:function(){this.resetInternals(),this.currentElements=a([])},prepareForm:function(){this.reset(),this.toHide=this.errors().add(this.containers)},prepareElement:function(a){this.reset(),this.toHide=this.errorsFor(a)},elementValue:function(b){var c,d,e=a(b),f=b.type,g="undefined"!=typeof e.attr("contenteditable")&&"false"!==e.attr("contenteditable");return"radio"===f||"checkbox"===f?this.findByName(b.name).filter(":checked").val():"number"===f&&"undefined"!=typeof b.validity?b.validity.badInput?"NaN":e.val():(c=g?e.text():e.val(),"file"===f?"C:\\fakepath\\"===c.substr(0,12)?c.substr(12):(d=c.lastIndexOf("/"),d>=0?c.substr(d+1):(d=c.lastIndexOf("\\"),d>=0?c.substr(d+1):c)):"string"==typeof c?c.replace(/\r/g,""):c)},check:function(b){b=this.validationTargetFor(this.clean(b));var c,d,e,f,g=a(b).rules(),h=a.map(g,function(a,b){return b}).length,i=!1,j=this.elementValue(b);"function"==typeof g.normalizer?f=g.normalizer:"function"==typeof this.settings.normalizer&&(f=this.settings.normalizer),f&&(j=f.call(b,j),delete g.normalizer);for(d in g){e={method:d,parameters:g[d]};try{if(c=a.validator.methods[d].call(this,j,b,e.parameters),"dependency-mismatch"===c&&1===h){i=!0;continue}if(i=!1,"pending"===c)return void(this.toHide=this.toHide.not(this.errorsFor(b)));if(!c)return this.formatAndAdd(b,e),!1}catch(k){throw this.settings.debug&&window.console&&console.log("Exception occurred when checking element "+b.id+", check the '"+e.method+"' method.",k),k instanceof TypeError&&(k.message+=".  Exception occurred when checking element "+b.id+", check the '"+e.method+"' method."),k}}if(!i)return this.objectLength(g)&&this.successList.push(b),!0},customDataMessage:function(b,c){return a(b).data("msg"+c.charAt(0).toUpperCase()+c.substring(1).toLowerCase())||a(b).data("msg")},customMessage:function(a,b){var c=this.settings.messages[a];return c&&(c.constructor===String?c:c[b])},findDefined:function(){for(var a=0;a<arguments.length;a++)if(void 0!==arguments[a])return arguments[a]},defaultMessage:function(b,c){"string"==typeof c&&(c={method:c});var d=this.findDefined(this.customMessage(b.name,c.method),this.customDataMessage(b,c.method),!this.settings.ignoreTitle&&b.title||void 0,a.validator.messages[c.method],"<strong>Warning: No message defined for "+b.name+"</strong>"),e=/\$?\{(\d+)\}/g;return"function"==typeof d?d=d.call(this,c.parameters,b):e.test(d)&&(d=a.validator.format(d.replace(e,"{$1}"),c.parameters)),d},formatAndAdd:function(a,b){var c=this.defaultMessage(a,b);this.errorList.push({message:c,element:a,method:b.method}),this.errorMap[a.name]=c,this.submitted[a.name]=c},addWrapper:function(a){return this.settings.wrapper&&(a=a.add(a.parent(this.settings.wrapper))),a},defaultShowErrors:function(){var a,b,c;for(a=0;this.errorList[a];a++)c=this.errorList[a],this.settings.highlight&&this.settings.highlight.call(this,c.element,this.settings.errorClass,this.settings.validClass),this.showLabel(c.element,c.message);if(this.errorList.length&&(this.toShow=this.toShow.add(this.containers)),this.settings.success)for(a=0;this.successList[a];a++)this.showLabel(this.successList[a]);if(this.settings.unhighlight)for(a=0,b=this.validElements();b[a];a++)this.settings.unhighlight.call(this,b[a],this.settings.errorClass,this.settings.validClass);this.toHide=this.toHide.not(this.toShow),this.hideErrors(),this.addWrapper(this.toShow).show()},validElements:function(){return this.currentElements.not(this.invalidElements())},invalidElements:function(){return a(this.errorList).map(function(){return this.element})},showLabel:function(b,c){var d,e,f,g,h=this.errorsFor(b),i=this.idOrName(b),j=a(b).attr("aria-describedby");h.length?(h.removeClass(this.settings.validClass).addClass(this.settings.errorClass),h.html(c)):(h=a("<"+this.settings.errorElement+">").attr("id",i+"-error").addClass(this.settings.errorClass).html(c||""),d=h,this.settings.wrapper&&(d=h.hide().show().wrap("<"+this.settings.wrapper+"/>").parent()),this.labelContainer.length?this.labelContainer.append(d):this.settings.errorPlacement?this.settings.errorPlacement.call(this,d,a(b)):d.insertAfter(b),h.is("label")?h.attr("for",i):0===h.parents("label[for='"+this.escapeCssMeta(i)+"']").length&&(f=h.attr("id"),j?j.match(new RegExp("\\b"+this.escapeCssMeta(f)+"\\b"))||(j+=" "+f):j=f,a(b).attr("aria-describedby",j),e=this.groups[b.name],e&&(g=this,a.each(g.groups,function(b,c){c===e&&a("[name='"+g.escapeCssMeta(b)+"']",g.currentForm).attr("aria-describedby",h.attr("id"))})))),!c&&this.settings.success&&(h.text(""),"string"==typeof this.settings.success?h.addClass(this.settings.success):this.settings.success(h,b)),this.toShow=this.toShow.add(h)},errorsFor:function(b){var c=this.escapeCssMeta(this.idOrName(b)),d=a(b).attr("aria-describedby"),e="label[for='"+c+"'], label[for='"+c+"'] *";return d&&(e=e+", #"+this.escapeCssMeta(d).replace(/\s+/g,", #")),this.errors().filter(e)},escapeCssMeta:function(a){return void 0===a?"":a.replace(/([\\!"#$%&'()*+,./:;<=>?@\[\]^`{|}~])/g,"\\$1")},idOrName:function(a){return this.groups[a.name]||(this.checkable(a)?a.name:a.id||a.name)},validationTargetFor:function(b){return this.checkable(b)&&(b=this.findByName(b.name)),a(b).not(this.settings.ignore)[0]},checkable:function(a){return/radio|checkbox/i.test(a.type)},findByName:function(b){return a(this.currentForm).find("[name='"+this.escapeCssMeta(b)+"']")},getLength:function(b,c){switch(c.nodeName.toLowerCase()){case"select":return a("option:selected",c).length;case"input":if(this.checkable(c))return this.findByName(c.name).filter(":checked").length}return b.length},depend:function(a,b){return!this.dependTypes[typeof a]||this.dependTypes[typeof a](a,b)},dependTypes:{"boolean":function(a){return a},string:function(b,c){return!!a(b,c.form).length},"function":function(a,b){return a(b)}},optional:function(b){var c=this.elementValue(b);return!a.validator.methods.required.call(this,c,b)&&"dependency-mismatch"},startRequest:function(b){this.pending[b.name]||(this.pendingRequest++,a(b).addClass(this.settings.pendingClass),this.pending[b.name]=!0)},stopRequest:function(b,c){this.pendingRequest--,this.pendingRequest<0&&(this.pendingRequest=0),delete this.pending[b.name],a(b).removeClass(this.settings.pendingClass),c&&0===this.pendingRequest&&this.formSubmitted&&this.form()&&0===this.pendingRequest?(a(this.currentForm).trigger("submit"),this.submitButton&&a("input:hidden[name='"+this.submitButton.name+"']",this.currentForm).remove(),this.formSubmitted=!1):!c&&0===this.pendingRequest&&this.formSubmitted&&(a(this.currentForm).triggerHandler("invalid-form",[this]),this.formSubmitted=!1)},previousValue:function(b,c){return c="string"==typeof c&&c||"remote",a.data(b,"previousValue")||a.data(b,"previousValue",{old:null,valid:!0,message:this.defaultMessage(b,{method:c})})},destroy:function(){this.resetForm(),a(this.currentForm).off(".validate").removeData("validator").find(".validate-equalTo-blur").off(".validate-equalTo").removeClass("validate-equalTo-blur").find(".validate-lessThan-blur").off(".validate-lessThan").removeClass("validate-lessThan-blur").find(".validate-lessThanEqual-blur").off(".validate-lessThanEqual").removeClass("validate-lessThanEqual-blur").find(".validate-greaterThanEqual-blur").off(".validate-greaterThanEqual").removeClass("validate-greaterThanEqual-blur").find(".validate-greaterThan-blur").off(".validate-greaterThan").removeClass("validate-greaterThan-blur")}},classRuleSettings:{required:{required:!0},email:{email:!0},url:{url:!0},date:{date:!0},dateISO:{dateISO:!0},number:{number:!0},digits:{digits:!0},creditcard:{creditcard:!0}},addClassRules:function(b,c){b.constructor===String?this.classRuleSettings[b]=c:a.extend(this.classRuleSettings,b)},classRules:function(b){var c={},d=a(b).attr("class");return d&&a.each(d.split(" "),function(){this in a.validator.classRuleSettings&&a.extend(c,a.validator.classRuleSettings[this])}),c},normalizeAttributeRule:function(a,b,c,d){/min|max|step/.test(c)&&(null===b||/number|range|text/.test(b))&&(d=Number(d),isNaN(d)&&(d=void 0)),d||0===d?a[c]=d:b===c&&"range"!==b&&(a["date"===b?"dateISO":c]=!0)},attributeRules:function(b){var c,d,e={},f=a(b),g=b.getAttribute("type");for(c in a.validator.methods)"required"===c?(d=b.getAttribute(c),""===d&&(d=!0),d=!!d):d=f.attr(c),this.normalizeAttributeRule(e,g,c,d);return e.maxlength&&/-1|2147483647|524288/.test(e.maxlength)&&delete e.maxlength,e},dataRules:function(b){var c,d,e={},f=a(b),g=b.getAttribute("type");for(c in a.validator.methods)d=f.data("rule"+c.charAt(0).toUpperCase()+c.substring(1).toLowerCase()),""===d&&(d=!0),this.normalizeAttributeRule(e,g,c,d);return e},staticRules:function(b){var c={},d=a.data(b.form,"validator");return d.settings.rules&&(c=a.validator.normalizeRule(d.settings.rules[b.name])||{}),c},normalizeRules:function(b,c){return a.each(b,function(d,e){if(e===!1)return void delete b[d];if(e.param||e.depends){var f=!0;switch(typeof e.depends){case"string":f=!!a(e.depends,c.form).length;break;case"function":f=e.depends.call(c,c)}f?b[d]=void 0===e.param||e.param:(a.data(c.form,"validator").resetElements(a(c)),delete b[d])}}),a.each(b,function(a,d){b[a]="function"==typeof d&&"normalizer"!==a?d(c):d}),a.each(["minlength","maxlength"],function(){b[this]&&(b[this]=Number(b[this]))}),a.each(["rangelength","range"],function(){var a;b[this]&&(Array.isArray(b[this])?b[this]=[Number(b[this][0]),Number(b[this][1])]:"string"==typeof b[this]&&(a=b[this].replace(/[\[\]]/g,"").split(/[\s,]+/),b[this]=[Number(a[0]),Number(a[1])]))}),a.validator.autoCreateRanges&&(null!=b.min&&null!=b.max&&(b.range=[b.min,b.max],delete b.min,delete b.max),null!=b.minlength&&null!=b.maxlength&&(b.rangelength=[b.minlength,b.maxlength],delete b.minlength,delete b.maxlength)),b},normalizeRule:function(b){if("string"==typeof b){var c={};a.each(b.split(/\s/),function(){c[this]=!0}),b=c}return b},addMethod:function(b,c,d){a.validator.methods[b]=c,a.validator.messages[b]=void 0!==d?d:a.validator.messages[b],c.length<3&&a.validator.addClassRules(b,a.validator.normalizeRule(b))},methods:{required:function(b,c,d){if(!this.depend(d,c))return"dependency-mismatch";if("select"===c.nodeName.toLowerCase()){var e=a(c).val();return e&&e.length>0}return this.checkable(c)?this.getLength(b,c)>0:void 0!==b&&null!==b&&b.length>0},email:function(a,b){return this.optional(b)||/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test(a)},url:function(a,b){return this.optional(b)||/^(?:(?:(?:https?|ftp):)?\/\/)(?:(?:[^\]\[?\/<~#`!@$^&*()+=}|:";',>{ ]|%[0-9A-Fa-f]{2})+(?::(?:[^\]\[?\/<~#`!@$^&*()+=}|:";',>{ ]|%[0-9A-Fa-f]{2})*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$/i.test(a)},date:function(){var a=!1;return function(b,c){return a||(a=!0,this.settings.debug&&window.console&&console.warn("The `date` method is deprecated and will be removed in version '2.0.0'.\nPlease don't use it, since it relies on the Date constructor, which\nbehaves very differently across browsers and locales. Use `dateISO`\ninstead or one of the locale specific methods in `localizations/`\nand `additional-methods.js`.")),this.optional(c)||!/Invalid|NaN/.test(new Date(b).toString())}}(),dateISO:function(a,b){return this.optional(b)||/^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/.test(a)},number:function(a,b){return this.optional(b)||/^(?:-?\d+|-?\d{1,3}(?:,\d{3})+)?(?:\.\d+)?$/.test(a)},digits:function(a,b){return this.optional(b)||/^\d+$/.test(a)},minlength:function(a,b,c){var d=Array.isArray(a)?a.length:this.getLength(a,b);return this.optional(b)||d>=c},maxlength:function(a,b,c){var d=Array.isArray(a)?a.length:this.getLength(a,b);return this.optional(b)||d<=c},rangelength:function(a,b,c){var d=Array.isArray(a)?a.length:this.getLength(a,b);return this.optional(b)||d>=c[0]&&d<=c[1]},min:function(a,b,c){return this.optional(b)||a>=c},max:function(a,b,c){return this.optional(b)||a<=c},range:function(a,b,c){return this.optional(b)||a>=c[0]&&a<=c[1]},step:function(b,c,d){var e,f=a(c).attr("type"),g="Step attribute on input type "+f+" is not supported.",h=["text","number","range"],i=new RegExp("\\b"+f+"\\b"),j=f&&!i.test(h.join()),k=function(a){var b=(""+a).match(/(?:\.(\d+))?$/);return b&&b[1]?b[1].length:0},l=function(a){return Math.round(a*Math.pow(10,e))},m=!0;if(j)throw new Error(g);return e=k(d),(k(b)>e||l(b)%l(d)!==0)&&(m=!1),this.optional(c)||m},equalTo:function(b,c,d){var e=a(d);return this.settings.onfocusout&&e.not(".validate-equalTo-blur").length&&e.addClass("validate-equalTo-blur").on("blur.validate-equalTo",function(){a(c).valid()}),b===e.val()},remote:function(b,c,d,e){if(this.optional(c))return"dependency-mismatch";e="string"==typeof e&&e||"remote";var f,g,h,i=this.previousValue(c,e);return this.settings.messages[c.name]||(this.settings.messages[c.name]={}),i.originalMessage=i.originalMessage||this.settings.messages[c.name][e],this.settings.messages[c.name][e]=i.message,d="string"==typeof d&&{url:d}||d,h=a.param(a.extend({data:b},d.data)),i.old===h?i.valid:(i.old=h,f=this,this.startRequest(c),g={},g[c.name]=b,a.ajax(a.extend(!0,{mode:"abort",port:"validate"+c.name,dataType:"json",data:g,context:f.currentForm,success:function(a){var d,g,h,j=a===!0||"true"===a;f.settings.messages[c.name][e]=i.originalMessage,j?(h=f.formSubmitted,f.resetInternals(),f.toHide=f.errorsFor(c),f.formSubmitted=h,f.successList.push(c),f.invalid[c.name]=!1,f.showErrors()):(d={},g=a||f.defaultMessage(c,{method:e,parameters:b}),d[c.name]=i.message=g,f.invalid[c.name]=!0,f.showErrors(d)),i.valid=j,f.stopRequest(c,j)}},d)),"pending")}}});var c,d={};return a.ajaxPrefilter?a.ajaxPrefilter(function(a,b,c){var e=a.port;"abort"===a.mode&&(d[e]&&d[e].abort(),d[e]=c)}):(c=a.ajax,a.ajax=function(b){var e=("mode"in b?b:a.ajaxSettings).mode,f=("port"in b?b:a.ajaxSettings).port;return"abort"===e?(d[f]&&d[f].abort(),d[f]=c.apply(this,arguments),d[f]):c.apply(this,arguments)}),a});;
/**
 * @license
 * Unobtrusive validation support library for jQuery and jQuery Validate
 * Copyright (c) .NET Foundation. All rights reserved.
 * Licensed under the Apache License, Version 2.0. See License.txt in the project root for license information.
 * @version v4.0.0
 */
!function(a){"function"==typeof define&&define.amd?define("jquery.validate.unobtrusive",["jquery-validation"],a):"object"==typeof module&&module.exports?module.exports=a(require("jquery-validation")):jQuery.validator.unobtrusive=a(jQuery)}(function(s){var a,o=s.validator,d="unobtrusiveValidation";function l(a,e,n){a.rules[e]=n,a.message&&(a.messages[e]=a.message)}function u(a){return a.replace(/([!"#$%&'()*+,./:;<=>?@\[\\\]^`{|}~])/g,"\\$1")}function n(a){return a.substr(0,a.lastIndexOf(".")+1)}function m(a,e){return a=0===a.indexOf("*.")?a.replace("*.",e):a}function f(a){var e=s(this),n="__jquery_unobtrusive_validation_form_reset";if(!e.data(n)){e.data(n,!0);try{e.data("validator").resetForm()}finally{e.removeData(n)}e.find(".validation-summary-errors").addClass("validation-summary-valid").removeClass("validation-summary-errors"),e.find(".field-validation-error").addClass("field-validation-valid").removeClass("field-validation-error").removeData("unobtrusiveContainer").find(">*").removeData("unobtrusiveContainer")}}function p(n){function a(a,e){(a=r[a])&&s.isFunction(a)&&a.apply(n,e)}var e=s(n),t=e.data(d),i=s.proxy(f,n),r=o.unobtrusive.options||{};return t||(t={options:{errorClass:r.errorClass||"input-validation-error",errorElement:r.errorElement||"span",errorPlacement:function(){!function(a,e){var e=s(this).find("[data-valmsg-for='"+u(e[0].name)+"']"),n=(n=e.attr("data-valmsg-replace"))?!1!==s.parseJSON(n):null;e.removeClass("field-validation-valid").addClass("field-validation-error"),a.data("unobtrusiveContainer",e),n?(e.empty(),a.removeClass("input-validation-error").appendTo(e)):a.hide()}.apply(n,arguments),a("errorPlacement",arguments)},invalidHandler:function(){!function(a,e){var n=s(this).find("[data-valmsg-summary=true]"),t=n.find("ul");t&&t.length&&e.errorList.length&&(t.empty(),n.addClass("validation-summary-errors").removeClass("validation-summary-valid"),s.each(e.errorList,function(){s("<li />").html(this.message).appendTo(t)}))}.apply(n,arguments),a("invalidHandler",arguments)},messages:{},rules:{},success:function(){!function(a){var e,n=a.data("unobtrusiveContainer");n&&(e=(e=n.attr("data-valmsg-replace"))?s.parseJSON(e):null,n.addClass("field-validation-valid").removeClass("field-validation-error"),a.removeData("unobtrusiveContainer"),e&&n.empty())}.apply(n,arguments),a("success",arguments)}},attachValidation:function(){e.off("reset."+d,i).on("reset."+d,i).validate(this.options)},validate:function(){return e.validate(),e.valid()}},e.data(d,t)),t}return o.unobtrusive={adapters:[],parseElement:function(t,a){var e,i,r,o=s(t),d=o.parents("form")[0];d&&((e=p(d)).options.rules[t.name]=i={},e.options.messages[t.name]=r={},s.each(this.adapters,function(){var a="data-val-"+this.name,e=o.attr(a),n={};void 0!==e&&(a+="-",s.each(this.params,function(){n[this]=o.attr(a+this)}),this.adapt({element:t,form:d,message:e,params:n,rules:i,messages:r}))}),s.extend(i,{__dummy__:!0}),a||e.attachValidation())},parse:function(a){var a=s(a),e=a.parents().addBack().filter("form").add(a.find("form")).has("[data-val=true]");a.find("[data-val=true]").each(function(){o.unobtrusive.parseElement(this,!0)}),e.each(function(){var a=p(this);a&&a.attachValidation()})}},(a=o.unobtrusive.adapters).add=function(a,e,n){return n||(n=e,e=[]),this.push({name:a,params:e,adapt:n}),this},a.addBool=function(e,n){return this.add(e,function(a){l(a,n||e,!0)})},a.addMinMax=function(a,t,i,r,e,n){return this.add(a,[e||"min",n||"max"],function(a){var e=a.params.min,n=a.params.max;e&&n?l(a,r,[e,n]):e?l(a,t,e):n&&l(a,i,n)})},a.addSingleVal=function(e,n,t){return this.add(e,[n||"val"],function(a){l(a,t||e,a.params[n])})},o.addMethod("__dummy__",function(a,e,n){return!0}),o.addMethod("regex",function(a,e,n){return!!this.optional(e)||(e=new RegExp(n).exec(a))&&0===e.index&&e[0].length===a.length}),o.addMethod("nonalphamin",function(a,e,n){var t;return t=n?(t=a.match(/\W/g))&&t.length>=n:t}),o.methods.extension?(a.addSingleVal("accept","mimtype"),a.addSingleVal("extension","extension")):a.addSingleVal("extension","extension","accept"),a.addSingleVal("regex","pattern"),a.addBool("creditcard").addBool("date").addBool("digits").addBool("email").addBool("number").addBool("url"),a.addMinMax("length","minlength","maxlength","rangelength").addMinMax("range","min","max","range"),a.addMinMax("minlength","minlength").addMinMax("maxlength","minlength","maxlength"),a.add("equalto",["other"],function(a){var e=n(a.element.name),e=m(a.params.other,e);l(a,"equalTo",s(a.form).find(":input").filter("[name='"+u(e)+"']")[0])}),a.add("required",function(a){"INPUT"===a.element.tagName.toUpperCase()&&"CHECKBOX"===a.element.type.toUpperCase()||l(a,"required",!0)}),a.add("remote",["url","type","additionalfields"],function(t){var i={url:t.params.url,type:t.params.type||"GET",data:{}},r=n(t.element.name);s.each((t.params.additionalfields||t.element.name).replace(/^\s+|\s+$/g,"").split(/\s*,\s*/g),function(a,e){var n=m(e,r);i.data[n]=function(){var a=s(t.form).find(":input").filter("[name='"+u(n)+"']");return a.is(":checkbox")?a.filter(":checked").val()||a.filter(":hidden").val()||"":a.is(":radio")?a.filter(":checked").val()||"":a.val()}}),l(t,"remote",i)}),a.add("password",["min","nonalphamin","regex"],function(a){a.params.min&&l(a,"minlength",a.params.min),a.params.nonalphamin&&l(a,"nonalphamin",a.params.nonalphamin),a.params.regex&&l(a,"regex",a.params.regex)}),a.add("fileextensions",["extensions"],function(a){l(a,"extension",a.params.extensions)}),s(function(){o.unobtrusive.parse(document)}),o.unobtrusive});;
(function ($) {
    delete $.validator.methods.email;

    var adapters = $.validator.unobtrusive.adapters;
    adapters.fxbAddNumberVal = function (adapterName, attribute, ruleName) {
        attribute = attribute || "val";
        ruleName = ruleName || adapterName;
        this.add(adapterName, [attribute], function(options) {
                var attrVal = options.params[attribute];
                if ((attrVal || attrVal === 0) && !isNaN(attrVal)) {
                    options.rules[ruleName] = Number(attrVal);
                }
                if (options.message) {
                    options.messages[ruleName] = options.message;
                }
            });
    };

    adapters.fxbAddMinMax = function(adapterName, minRuleName, maxRuleName, minAttribute, maxAttribute) {
        minAttribute = minAttribute || "min";
        maxAttribute = maxAttribute || "max";
        this.add(adapterName, [minAttribute, maxAttribute], function(options) {
                if (options.params[minAttribute] && options.params[maxAttribute]) {
                    if (!options.rules.hasOwnProperty(minRuleName)) {
                        if (options.message) {
                            options.messages[minRuleName] = options.message;
                        }
                    }
                    if (!options.rules.hasOwnProperty(maxRuleName)) {
                        if (options.message) {
                            options.messages[maxRuleName] = options.message;
                        }
                    }
                }
            });
    };

    adapters.addBool("ischecked", "required");

    $.validator.addMethod(
        "daterange",
        function(value, element, params) {
            return this.optional(element) || (value >= params.min && value <= params.max);
        });

    adapters.add(
        "daterange",
        ["min", "max"],
        function(options) {
            var params = {
                min: options.params.min,
                max: options.params.max
            };
            options.rules["daterange"] = params;
            options.messages["daterange"] = options.message;
        });

    adapters.addSingleVal("filesize", "max");
    $.validator.addMethod(
        "filesize",
        function (value, element, max) {
            if (!this.optional(element)) {
                for (var i = 0; i < element.files.length; i++) {
                    if (element.files[i].size > max) {
                        return false;
                    }
                }
            }
            return true;
        });

    adapters.addSingleVal("filecount", "max");
    $.validator.addMethod(
        "filecount",
        function (value, element, max) {
            if (!this.optional(element)) {
                    if (element.files.length > max) {
                        return false;
                    }
            }
            return true;
        });

    adapters.addSingleVal("filetype", "allowedcontenttypes");
    $.validator.addMethod(
        "filetype",
        function (value, element, allowedContentTypes) {
            if (!this.optional(element)) {
                var allowedContentTypesArray = allowedContentTypes.split(",").filter(function (s) {
                    // Remove empty entries
                    return s !== "";
                });
                if (allowedContentTypesArray.length) {
                    for (var i = 0; i < element.files.length; i++) {
                        var file = element.files[i];
                        var isValid = false;
                        for (var j = 0; j < allowedContentTypesArray.length; j++) {
                            var allowedContentType = allowedContentTypesArray[j];
                            if (allowedContentType.indexOf("/") !== -1) {
                                // MIME type comparison if there is a slash "/"
                                isValid = allowedContentType.toLowerCase() === file.type.toLowerCase();
                            } else {
                                // File extension comparison
                                isValid = allowedContentType.toLowerCase() === "." + file.name.split(".").pop().toLowerCase();
                            }

                            if (isValid) {
                                break;
                            }
                        }

                        if (!isValid) {
                            return false;
                        }
                    }
                }
            }
            return true;
        });

    adapters.fxbAddNumberVal("min");
    adapters.fxbAddNumberVal("max");
    adapters.fxbAddNumberVal("step");

    adapters.fxbAddMinMax("range", "min", "max");
    adapters.fxbAddMinMax("length", "minlength", "maxlength");
    adapters.fxbAddMinMax("daterange", "min", "max");
})(jQuery);
;
(function($) {
    var eventIds = {
        fieldCompleted: "2ca692cb-bdb2-4c9d-a3b5-917b3656c46a",
        fieldError: "ea27aca5-432f-424a-b000-26ba5f8ae60a"
    };

    function endsWith(str, suffix) {
        return str.toLowerCase().indexOf(suffix.toLowerCase(), str.length - suffix.length) !== -1;
    }

    function getOwner(form, elementId) {
        var targetId = elementId.slice(0, -(elementId.length - elementId.lastIndexOf(".") - 1)) + "Value";
        return form.find("input[name=\"" + targetId + "\"]")[0];
    }

    function getSessionId(form) {
        var formId = form[0].id;
        var targetId = formId.slice(0, -(formId.length - formId.lastIndexOf("_") - 1)) + "FormSessionId";
        var element = form.find("input[type='hidden'][id=\"" + targetId + "\"]");
        return element.val();
    }

    function getElementName(element) {
        var fieldName = element.name;
        if (!endsWith(fieldName, "value")) {
            return getFieldGuid(fieldName) + "Value";
        }

        return fieldName;
    }

    function getElementValue(element) {
        var value;
        if (element.type === "checkbox" || element.type === "radio") {
            var form = $(element).closest("form");
            var checkboxList = form.find("input[name='" + element.name + "']");
            if (checkboxList.length > 1) {
                value = [];
                checkboxList = checkboxList.not(":not(:checked)");
                $.each(checkboxList, function () {
                    value.push($(this).val());
                });
            } else {
                value = element.checked ? "1" : "0";
            }
        } else {
            value = $(element).val();
        }

        if (value && Object.prototype.toString.call(value) === "[object Array]") {
            value = value.join(",");
        }

        return value;
    }

    function getFieldGuid(fieldName) {
        var searchPattern = "fields[";
        var index = fieldName.toLowerCase().indexOf(searchPattern);
        return fieldName.substring(0, index + searchPattern.length + 38);
    }

    function getFieldName(element) {
        return $(element).attr("data-sc-field-name");
    }

    $.fxbFormTracker = function (el, options) {
        this.el = el;
        this.$el = $(el);
        this.options = $.extend({}, $.fxbFormTracker.defaultOptions, options);
        this.init();
    },

        $.fxbFormTracker.parse = function (formId) {
            var $form = $(formId);
            $form.track_fxbForms();

            var isSessionExpired = parseInt($("[name$='.IsSessionExpired']").val());
            if (isSessionExpired) {
                alert($.fxbFormTracker.texts.expiredWebSession);
            }
        },

        $.extend($.fxbFormTracker,
            {
                defaultOptions: {
                    formId: null,
                    sessionId: null,
                    fieldId: null,
                    fieldValue: null,
                    duration: null
                },

                prototype: {
                    init: function () {
                        this.options.duration = 0;
                        this.options.formId = this.$el.attr("data-sc-fxb");
                    },

                    startTracking: function () {
                        this.options.sessionId = getSessionId(this.$el);

                        var self = this;
                        var inputs = this.$el.find("input:not([type='submit']), select, textarea");
                        var trackedInputs = inputs.filter("[data-sc-tracking='True'], [data-sc-tracking='true']");
                        var trackedNonDateInputs = trackedInputs.not("[type='date']");

                        if (trackedInputs.length) {
                            inputs.not(trackedInputs).on("focus",
                                function () {
                                    self.onFocusField(this);
                                });

                            trackedInputs.on("focus",
                                function () {
                                    self.onFocusField(this, true);
                                }).on("blur",
                                    function () {
                                        self.onBlurField(this);
                                    });

                            trackedNonDateInputs.on("change",
                                function () {
                                    self.onBlurField(this);
                                });
                        }
                    },

                    onFocusField: function (element, hasTracking) {
                        if (!hasTracking) {
                            this.options.fieldId = "";
                            return;
                        }

                        var fieldId = getElementName(element);

                        if (this.options.fieldId !== fieldId) {
                            this.options.fieldId = fieldId;
                            this.options.duration = $.now();
                            this.options.fieldValue = getElementValue(element);
                        }
                    },

                    onBlurField: function (element) {
                        var fieldId = getElementName(element);
                        var timeStamp = $.now();

                        if (!endsWith(fieldId, "value")) {
                            var owner = getOwner(this.$el, fieldId);
                            if (!owner) {
                                return;
                            }

                            element = owner;
                        }

                        var duration = this.options.duration ? Math.round((timeStamp - this.options.duration) / 1000) : 0;
                        var value = getElementValue(element);
                        var fieldChanged = this.options.fieldId !== fieldId;
                        if (fieldChanged) {
                            this.options.fieldId = fieldId;
                            this.options.duration = $.now();
                            duration = 0;
                        }
                        if (fieldChanged || this.options.fieldValue !== value) {
                            this.options.fieldValue = value;

                            var fieldName = getFieldName(element);
                            var clientEvent = this.buildEvent(fieldId, fieldName, eventIds.fieldCompleted, duration);

                            var validator = this.$el.data("validator");
                            var validationEvents = [];
                            if (validator && !validator.element(element)) {
                                validationEvents = this.checkClientValidation(element, fieldName, validator, duration);
                            }

                            this.trackEvents($.merge([clientEvent], validationEvents));
                        }
                    },

                    buildEvent: function (fieldId, fieldName, eventId, duration) {
                        var fieldIdHidden = getFieldGuid(fieldId) + "ItemId";

                        fieldId = $("input[name=\"" + fieldIdHidden + "\"]").val();

                        return {
                            'formId': this.options.formId,
                            'sessionId': this.options.sessionId,
                            'eventId': eventId,
                            'fieldId': fieldId,
                            'duration': duration,
                            'fieldName': fieldName
                        };
                    },

                    checkClientValidation: function (element, fieldName, validator, duration) {
                        var tracker = this;
                        var events = [];

                        $.each(validator.errorMap,
                            function (key) {
                                if (key === element.name) {
                                    var clientEvent = tracker.buildEvent(key, fieldName, eventIds.fieldError, duration);
                                    events.push(clientEvent);
                                }
                            });

                        return events;
                    },

                    trackEvents: function (events) {
                        $.ajax({
                            type: "POST",
                            url: "/fieldtracking/register",
                            data: JSON.stringify(events),
                            contentType: "application/json"
                        }).done(function (data, textStatus, jqXhr) {
                            if ((jqXhr.statusText === "OK" || jqXhr.statusText === "success") && jqXhr.responseText !== "") {
                                alert(jqXhr.responseText);
                            }
                        });
                    }
                }
            });

    $.fn.track_fxbForms = function (options) {
        return this.each(function () {
            var tracker = $.data(this, "fxbForms.tracking");
            if (tracker) {
                tracker.startTracking();
            } else {
                tracker = new $.fxbFormTracker(this, options);
                $.data(this, "fxbForms.tracking", tracker);
                tracker.startTracking();
            }
        });
    };

    $("form[data-sc-fxb]").track_fxbForms();
})(jQuery);;
(function($) {
    $.fxbConditions = function(el, options) {
            this.el = el;
            this.$el = $(el);
            this.options = $.extend({}, $.fxbConditions.defaultOptions, options);
    },
        $.fxbConditions.parse = function (formId) {
            var $form = $(formId);
            $form.init_formConditions();
        },

        $.extend($.fxbConditions,
            {
                defaultOptions: {
                    fieldConditions: [],
                    animate: true
                },

                helpers: {
                    normalize: function(value, preserveCase) {
                        if (value == null) {
                            return "";
                        }

                        return preserveCase ? String(value) : String(value).toLowerCase();
                    },

                    toNumber: function(value) {
                        value = Number(value);
                        return isNaN(value) ? undefined : value;
                    },

                    indexOf: function(str, value, startIndex, preserveCase) {
                        str = this.normalize(str, preserveCase);
                        value = this.normalize(value, preserveCase);

                        return str.indexOf(value, startIndex);
                    },

                    endsWith: function(str, value, preserveCase) {
                        str = this.normalize(str, preserveCase);
                        value = this.normalize(value, preserveCase);

                        var lengthDiff = str.length - value.length;
                        return lengthDiff >= 0 && str.substring(lengthDiff) === value;
                    }
                },

                actions: {
                    show: function($target) {
                        if (this.loaded && this.options.animate) {
                            if ($target.is(":hidden")) {
                                var $self = this;
                                $target.slideDown(function () {
                                    $self.setRequired($target);
                                });

                                return;
                            }
                        } else {
                            $target.show();
                        }

                        this.setRequired($target);
                    },

                    hide: function($target) {
                        if (this.loaded && this.options.animate) {
                            if ($target.is(":visible")) {
                                var $self = this;
                                $target.slideUp(function() {
                                    $self.setRequired($target);
                                });

                                return;
                            }
                        } else {
                            $target.hide();
                        }

                        this.setRequired($target);
                    },

                    enable: function($target) {
                        if ($target.is("input,select,textarea,button")) {
                            $target.prop("disabled", false);
                            this.setRequired($target);
                            $('[data-valmsg-for="' + $target.prop("name") + '"]').show();
                        }
                    },

                    disable: function($target) {
                        if ($target.is("input,select,textarea,button")) {
                            $target.prop("disabled", true);
                            this.setRequired($target);
                            $('[data-valmsg-for="' + $target.prop("name") + '"]').hide();
                        }
                    },

                    "go to page": function($target, action, conditionsResult) {
                        $target.each(function(idx, target) {
                            if (target.name &&
                                target.name.length &&
                                $(target).is("input[type='submit'], button[type='submit']")) {
                                var $nextPageEl = this.$el.find("[name=\"" + target.name + "\"][data-sc-next-page]");
                                if (!$nextPageEl.length) {
                                    if (conditionsResult && action.value) {
                                        var $currentEl = this.$el.find("[name=\"" + target.name + "\"]");
                                        $('<input>').attr({
                                            type: 'hidden',
                                            name: target.name,
                                            value: action.value,
                                            'data-sc-next-page': ""
                                        }).insertAfter($currentEl.last());
                                    }

                                    return;
                                }

                                var value = action.value;
                                if (!conditionsResult) {
                                    value = $nextPageEl.data("sc-next-page");

                                    for (var i = (this.executedActions.length - 1); i >= 0; i--) {
                                        var prevAction = this.executedActions[i];
                                        if (prevAction.fieldId === action.fieldId &&
                                            prevAction.conditionsResult &&
                                            prevAction.actionType.toLowerCase() === "go to page") {
                                            value = prevAction.value;
                                            break;
                                        }
                                    }
                                }

                                $nextPageEl.val(value);
                                $nextPageEl.prop("disabled", !value);
                            }
                        }.bind(this));
                    },

                    // action pairs used for finding the opposite action to execute when conditions are not satisfied
                    actionLinks: {
                        show: "hide",
                        enable: "disable",
                        "go to page": "go to page"
                    },

                    addAction: function(actionName, actionFn, oppositeActionName, oppositeActionFn) {
                        if (actionName && actionName.length) {
                            actionName = actionName.toLowerCase();

                            this[actionName] = actionFn;

                            if (arguments.length === 2) {
                                return;
                            }

                            if (oppositeActionName && oppositeActionName.length) {
                                oppositeActionName = oppositeActionName.toLowerCase();

                                this.actionLinks[actionName] = oppositeActionName;
                                if (arguments.length > 3) {
                                    this[oppositeActionName] = oppositeActionFn;
                                }
                            } else {
                                delete this.actionLinks[actionName];
                            }
                        }
                    },

                    getAction: function(actionName, conditionsResult) {
                        if (actionName && actionName.length) {
                            actionName = actionName.toLowerCase();

                            if (conditionsResult) {
                                return this[actionName];
                            }

                            if (this.actionLinks.hasOwnProperty(actionName)) {
                                var oppositeActionName = this.actionLinks[actionName];
                                return this[oppositeActionName];
                            } else {
                                for (var property in this.actionLinks) {
                                    if (this.actionLinks.hasOwnProperty(property) &&
                                        this.actionLinks[property] === actionName) {
                                        return this[property];
                                    }
                                }
                            }
                        }

                        return this[actionName];
                    }
                },

                operators: {
                    "contains": function(conditionValue, fieldValue) {
                        return $.fxbConditions.helpers.indexOf(fieldValue, conditionValue) >= 0;
                    },

                    "does not contain": function(conditionValue, fieldValue) {
                        return $.fxbConditions.helpers.indexOf(fieldValue, conditionValue) === -1;
                    },

                    "starts with": function(conditionValue, fieldValue) {
                        return $.fxbConditions.helpers.indexOf(fieldValue, conditionValue) === 0;
                    },

                    "does not start with": function(conditionValue, fieldValue) {
                        return $.fxbConditions.helpers.indexOf(fieldValue, conditionValue) !== 0;
                    },

                    "ends with": function(conditionValue, fieldValue) {
                        return $.fxbConditions.helpers.endsWith(fieldValue, conditionValue);
                    },

                    "does not end with": function(conditionValue, fieldValue) {
                        return !$.fxbConditions.helpers.endsWith(fieldValue, conditionValue);
                    },

                    "is equal to": function(conditionValue, fieldValue) {
                        conditionValue = $.fxbConditions.helpers.normalize(conditionValue);
                        fieldValue = $.fxbConditions.helpers.normalize(fieldValue);
                        if (fieldValue === conditionValue) {
                            return true;
                        }

                        if (conditionValue.length) {
                            var left = $.fxbConditions.helpers.toNumber(conditionValue);
                            if (typeof left === "number") {
                                var right = $.fxbConditions.helpers.toNumber(fieldValue);
                                return typeof right === "number" && left === right;
                            }
                        }

                        return false;
                    },

                    "is not equal to": function(conditionValue, fieldValue) {
                        conditionValue = $.fxbConditions.helpers.normalize(conditionValue);
                        fieldValue = $.fxbConditions.helpers.normalize(fieldValue);
                        if (fieldValue === conditionValue) {
                            return false;
                        }

                        if (conditionValue.length) {
                            var left = $.fxbConditions.helpers.toNumber(conditionValue);
                            if (typeof left === "number") {
                                var right = $.fxbConditions.helpers.toNumber(fieldValue);
                                return typeof right !== "number" || left !== right;
                            }
                        }

                        return true;
                    },

                    "is greater than": function(conditionValue, fieldValue) {
                        conditionValue = $.fxbConditions.helpers.normalize(conditionValue);
                        fieldValue = $.fxbConditions.helpers.normalize(fieldValue);

                        if (conditionValue.length) {
                            var left = $.fxbConditions.helpers.toNumber(conditionValue);
                            if (typeof left === "number") {
                                var right = $.fxbConditions.helpers.toNumber(fieldValue);
                                return typeof right === "number" && right > left;
                            }
                        }

                        return fieldValue > conditionValue;
                    },

                    "is greater than or equal to": function(conditionValue, fieldValue) {
                        conditionValue = $.fxbConditions.helpers.normalize(conditionValue);
                        fieldValue = $.fxbConditions.helpers.normalize(fieldValue);

                        if (fieldValue === conditionValue) {
                            return true;
                        }

                        if (conditionValue.length) {
                            var left = $.fxbConditions.helpers.toNumber(conditionValue);
                            if (typeof left === "number") {
                                var right = $.fxbConditions.helpers.toNumber(fieldValue);
                                return typeof right === "number" && right >= left;
                            }
                        }

                        return fieldValue >= conditionValue;
                    },

                    "is less than": function(conditionValue, fieldValue) {
                        conditionValue = $.fxbConditions.helpers.normalize(conditionValue);
                        fieldValue = $.fxbConditions.helpers.normalize(fieldValue);

                        if (conditionValue.length) {
                            var left = $.fxbConditions.helpers.toNumber(conditionValue);
                            if (typeof left === "number") {
                                var right = $.fxbConditions.helpers.toNumber(fieldValue);
                                return typeof right === "number" && right < left;
                            }
                        }

                        return fieldValue < conditionValue;
                    },

                    "is less than or equal to": function(conditionValue, fieldValue) {
                        conditionValue = $.fxbConditions.helpers.normalize(conditionValue);
                        fieldValue = $.fxbConditions.helpers.normalize(fieldValue);

                        if (fieldValue === conditionValue) {
                            return true;
                        }

                        if (conditionValue.length) {
                            var left = $.fxbConditions.helpers.toNumber(conditionValue);
                            if (typeof left === "number") {
                                var right = $.fxbConditions.helpers.toNumber(fieldValue);
                                return typeof right === "number" && right <= left;
                            }
                        }

                        return fieldValue <= conditionValue;
                    },

                    addOperator: function(operatorName, operatorFn) {
                        if (operatorName && operatorName.length) {
                            this[operatorName.toLowerCase()] = operatorFn;
                        }
                    },

                    getOperator: function(operatorName) {
                        return operatorName && operatorName.length ? this[operatorName.toLowerCase()] : null;
                    }
                },

                prototype: {
                    initConditions: function(options) {
                        this.options = $.extend(true, this.options || {}, options);

                        if (!this.options.fieldConditions) {
                            return;
                        }

                        var sourceFields = [];
                        this.options.fieldConditions.forEach(function(fieldCondition) {
                            if (!fieldCondition || !fieldCondition.conditions) {
                                return;
                            }

                            fieldCondition.conditions.forEach(function(condition) {
                                if (condition.fieldId && sourceFields.indexOf(condition.fieldId) === -1) {
                                    sourceFields.push(condition.fieldId);
                                    var $source = this.$el.find("[data-sc-field-key=\"" + condition.fieldId + "\"]")
                                        .filter(function() {
                                            return $.fxbConditions.helpers.endsWith(this.name, "value");
                                        });
                                    if ($source.length) {
                                        $source.on("change", this.applyConditions.bind(this));
                                    }
                                }
                            }.bind(this));
                        }.bind(this));

                        this.applyConditions();
                        this.loaded = true;
                    },

                    applyConditions: function() {
                        if (!this.options.fieldConditions) {
                            return;
                        }

                        this.executedActions = [];
                        this.fieldActions = {};

                        this.options.fieldConditions.forEach(function(fieldCondition) {
                            if (fieldCondition && fieldCondition.actions && fieldCondition.actions.length) {
                                var conditionsResult = this.evaluateConditions(fieldCondition);
                                fieldCondition.actions.forEach(function(action) {
                                    this.gatherFieldActions(action, conditionsResult);
                                }.bind(this));
                            }
                        }.bind(this));

                        for (var fieldId in this.fieldActions) {
                            if (!this.fieldActions.hasOwnProperty(fieldId)) continue;
                            for (var actionType in this.fieldActions[fieldId]) {
                                if (!this.fieldActions[fieldId].hasOwnProperty(actionType)) continue;
                                var action = this.fieldActions[fieldId][actionType].action;
                                var conditionsResult = this.fieldActions[fieldId][actionType].conditionsResult;
                                this.executeAction(action, conditionsResult);
                            }
                        }
                    },

                    setRequired: function($targets) {
                        $targets.each(function(idx, target) {
                            var $target = $(target);
                            if ($target.is("input:not([type='submit']), select, textarea")) {
                                var name = target.name;
                                if (!$.fxbConditions.helpers.endsWith(name, "value") && !$.fxbConditions.helpers.endsWith(name, "Files") )
                                    return;

                                name = name.slice(0, -(name.length - name.lastIndexOf(".") - 1)) + "Required";
                                var $requiredEl = this.$el.find("[name=\"" + name + "\"][data-sc-conditions-required]"),
                                    isNotAccessible = $target.is(":hidden") ||
                                        $target.css("visibility") === "hidden" ||
                                        target.disabled;

                                if (!$requiredEl.length) {
                                    if (isNotAccessible) {
                                        var $currentEl = this.$el.find("[name=\"" + target.name + "\"]");
                                        $('<input>').attr({
                                            type: 'hidden',
                                            name: name,
                                            value: false,
                                            "data-sc-conditions-required": ""
                                        }).insertAfter($currentEl.last());
                                    }

                                    return;
                                }

                                $requiredEl.val(false);
                                $requiredEl.prop("disabled", !isNotAccessible);
                            } else {
                                this.setRequired($target.find("input:not([type='submit']), select, textarea"));
                            }
                        }.bind(this));
                    },

                    executeAction: function(action, conditionsResult) {
                        if (action && action.fieldId && action.actionType) {
                            var $target = this.$el.find("[data-sc-field-key=\"" + action.fieldId + "\"]");
                            if ($target.length) {
                                var actionFn = $.fxbConditions.actions.getAction(action.actionType, conditionsResult);
                                if (actionFn && typeof actionFn === "function") {
                                    actionFn.call(this, $target, action, conditionsResult);
                                    var executedAction = $.extend(true,
                                        action,
                                        {
                                            conditionsResult: conditionsResult
                                        });
                                    this.executedActions.push(executedAction);
                                }
                            }
                        }
                    },

                    evaluateConditions: function(fieldCondition) {
                        if (!fieldCondition || !fieldCondition.conditions) return true;

                        var matchType = (fieldCondition.matchType || "").toLowerCase();
                        switch (matchType) {
                        case "all":
                            return fieldCondition.conditions.every(this.isConditionSatisfied.bind(this));
                        case "any":
                        default:
                            return fieldCondition.conditions.some(this.isConditionSatisfied.bind(this));
                        }
                    },

                    gatherFieldActions: function(action, conditionsResult) {
                        if (action && action.fieldId && action.actionType) {
                            if (typeof this.fieldActions[action.fieldId] === "undefined") {
                                this.fieldActions[action.fieldId] = {};
                            }

                            if (typeof this.fieldActions[action.fieldId][action.actionType] === "undefined") {
                                this.fieldActions[action.fieldId][action.actionType] = {
                                    action: action,
                                    conditionsResult: conditionsResult
                                };
                            }
                            // if a true conditionsResult finally appears for this particular fieldId and actionType, set it to true.
                            // from now on, it can never be set back to false again.
                            // (existing is deleted first to ensure this latest action appears at the bottom of the queue)
                            else if (!this.fieldActions[action.fieldId][action.actionType].conditionsResult && conditionsResult) {
                                delete this.fieldActions[action.fieldId][action.actionType];
                                this.fieldActions[action.fieldId][action.actionType] = {
                                    action: action,
                                    conditionsResult: true
                                };
                            }
                        }
                    },

                    getValueList: function(fieldId) {
                        var $fieldEl = this.$el.find("[data-sc-field-key=\"" + fieldId + "\"]").filter(function() {
                            return $.fxbConditions.helpers.endsWith(this.name, "value");
                        });

                        var $listElements = $fieldEl.filter(function(idx, element) {
                            return element.type === "checkbox" || element.type === "radio";
                        });

                        if (!$listElements.length && $fieldEl.prop("multiple")) {
                            $listElements = $fieldEl.find("option");
                        }

                        var value;
                        if ($listElements.length) {
                            if ($listElements.length > 1) {
                                value = $listElements.filter(":checked").map(function() {
                                    return $(this).val();
                                }).get();
                                if (!value.length) {
                                    value.push("");
                                }
                            } else {
                                value = [$listElements[0].checked ? "true" : "false"];
                            }
                        } else {
                            value = [$fieldEl.val()];
                        }

                        return value;
                    },

                    isConditionSatisfied: function(condition) {
                        if (condition && condition.operator) {
                            var operatorFn = $.fxbConditions.operators.getOperator(condition.operator);
                            if (operatorFn && typeof operatorFn === "function") {

                                var valueList = this.getValueList(condition.fieldId);
                                var result = condition.operator === "is not equal to"
                                    ? valueList.every(operatorFn.bind(this, condition.value))
                                    : valueList.some(operatorFn.bind(this, condition.value));
                                return result;
                            };
                        }

                        return false;
                    }
                }
            });

    $.fn.init_fxbConditions = function(options) {
        return this.each(function() {
            var conditions = $.data(this, "fxbForms.conditions");
            if (conditions) {
                conditions.initConditions(options);
            } else {
                conditions = new $.fxbConditions(this, options);
                $.data(this, "fxbForms.conditions", conditions);
                conditions.initConditions();
            }
        });
    };

    $.fn.init_formConditions = function() {
        var input = this.find('input[data-sc-fxb-condition]');
        if (input) {
            var conditions = JSON.parse(input.attr('value'));
            if (conditions) {
                if (typeof this.init_fxbConditions === 'function') {
                    this.init_fxbConditions(conditions);
                }
            }
        }
    };

    var forms = $("form[data-sc-fxb]");
    if (forms.length) {
        forms.each(function () {
            var formEl = $(this);
            formEl.init_formConditions();
        }).parent().on("submit", "form[data-sc-fxb]", function () {
            var $submitBtns = $(this).find("input[type='submit'], button[type='submit']");
            if ($submitBtns.length) {
                $submitBtns.on("click", function () {
                    return false;
                });
            }
        });
    }
})(jQuery);;
$.validator.setDefaults({ ignore: ":hidden:not(.fxt-captcha)" });

/**
 * Google Recaptcha
 */
var reCaptchaArray = reCaptchaArray || [];
$.validator.unobtrusive.adapters.add("recaptcha", function (options) {
    options.rules["recaptcha"] = true;
    if (options.message) {
        options.messages["recaptcha"] = options.message;
    }
});

$.validator.addMethod("recaptcha", function (value, element, exclude) {
    return true;
});
var recaptchasRendered = false;
var loadReCaptchas = function () {
    for (var i = 0; i < reCaptchaArray.length; i++) {
        var reCaptcha = reCaptchaArray[i];
        if (reCaptcha.IsRendered === undefined) {
            reCaptcha.IsRendered = true;
            reCaptcha();
        }
    }
};

/**
 * File upload Content Type
 */
$.validator.unobtrusive.adapters.addSingleVal("contenttype", "allowedcontenttypes");

$.validator.addMethod("contenttype", function (value, element, allowedcontenttypes) {
    if (!this.optional(element)) {
        for (var i = 0; i < element.files.length; i++) {
            if (allowedcontenttypes.indexOf(element.files[i].type) < 0) {
                return false;
            }
        }
    }
    return true;
});

/**
 * File upload File Size
 */
$.validator.unobtrusive.adapters.addSingleVal("filesize", "maxfilesize");
$.validator.addMethod("filesize", function (value, element, maxfilesize) {
    if (!this.optional(element)) {
        for (var i = 0; i < element.files.length; i++) {
            if (element.files[i].size > maxfilesize) {
                return false;
            }
        }
    }
    return true;
});

// Date Time Span Validator
["timespan", "tsminagedate", "tsfuturedate", "tspastdate"].forEach(validationType =>{
  $.validator.unobtrusive.adapters.add(validationType, ['min', 'max', 'unit'], function(options) {
    options.rules[validationType] = [options.params.min, options.params.max, options.params.unit];
    options.messages[validationType] = options.message;
  });
  
  $.validator.addMethod(validationType, function (value, element, params) {
    if (!this.optional(element)) {
      var unit = params[2];
      var minvalue = params[0];
      var maxvalue = params[1];
  
      var valueToValidate = 0;
  
      switch (unit) {
        case 'days':
          valueToValidate = getDays(value);
          break;
        case 'months':
          valueToValidate = getMonths(value);
          break;
        case 'years':
          valueToValidate = getYears(value);
          break;
      }
  
      var isValid = true;
  
      if (typeof minvalue !== 'undefined' && valueToValidate < minvalue)
        isValid = false;
  
      if (typeof maxvalue !== 'undefined' && valueToValidate > maxvalue)
        isValid = false;
  
      return isValid;
    }
    return true;
  });
})

/*
$.validator.unobtrusive.adapters.add('timespan', ['min', 'max', 'unit'], function(options) {
  options.rules['timespan'] = [options.params.min, options.params.max, options.params.unit];
  options.messages['timespan'] = options.message;
});

$.validator.addMethod("timespan", timespanValidatorFunction);*/

function getDays(date) {
  var today = new Date();
  return Math.floor((today - new Date(date)) / (1000 * 60 * 60 * 24));
}

function getYears(date) {
  var today = new Date();
  var diffYears = today.getFullYear() - new Date(date).getFullYear();
  var temp = today;

  temp.setFullYear(temp.getFullYear() - diffYears);

  if (new Date(date) > temp)
    diffYears--;

  return diffYears;
}

function getMonths(date) {
  var today = new Date();
  var d = new Date(date);

  return (today.getFullYear() - d.getFullYear()) * 12 + today.getMonth() - d.getMonth();
};
/*!
 * Signature Pad v4.1.5 | https://github.com/szimek/signature_pad
 * (c) 2023 Szymon Nowak | Released under the MIT license
 */
!function (t, e) {
    "object" == typeof exports && "undefined" != typeof module ? module.exports = e() : "function" == typeof define && define.amd ? define(e) : (t = "undefined" != typeof globalThis ? globalThis : t || self).SignaturePad = e()
}(this, (function () {
    "use strict";

    class t {
        constructor(t, e, i, s) {
            if (isNaN(t) || isNaN(e)) throw new Error(`Point is invalid: (${t}, ${e})`);
            this.x = +t, this.y = +e, this.pressure = i || 0, this.time = s || Date.now()
        }

        distanceTo(t) {
            return Math.sqrt(Math.pow(this.x - t.x, 2) + Math.pow(this.y - t.y, 2))
        }

        equals(t) {
            return this.x === t.x && this.y === t.y && this.pressure === t.pressure && this.time === t.time
        }

        velocityFrom(t) {
            return this.time !== t.time ? this.distanceTo(t) / (this.time - t.time) : 0
        }
    }

    class e {
        constructor(t, e, i, s, n, o) {
            this.startPoint = t, this.control2 = e, this.control1 = i, this.endPoint = s, this.startWidth = n, this.endWidth = o
        }

        static fromPoints(t, i) {
            const s = this.calculateControlPoints(t[0], t[1], t[2]).c2,
                n = this.calculateControlPoints(t[1], t[2], t[3]).c1;
            return new e(t[1], s, n, t[2], i.start, i.end)
        }

        static calculateControlPoints(e, i, s) {
            const n = e.x - i.x, o = e.y - i.y, h = i.x - s.x, r = i.y - s.y, a = (e.x + i.x) / 2, d = (e.y + i.y) / 2,
                c = (i.x + s.x) / 2, l = (i.y + s.y) / 2, u = Math.sqrt(n * n + o * o), v = Math.sqrt(h * h + r * r),
                _ = v / (u + v), m = c + (a - c) * _, p = l + (d - l) * _, g = i.x - m, w = i.y - p;
            return {c1: new t(a + g, d + w), c2: new t(c + g, l + w)}
        }

        length() {
            let t, e, i = 0;
            for (let s = 0; s <= 10; s += 1) {
                const n = s / 10,
                    o = this.point(n, this.startPoint.x, this.control1.x, this.control2.x, this.endPoint.x),
                    h = this.point(n, this.startPoint.y, this.control1.y, this.control2.y, this.endPoint.y);
                if (s > 0) {
                    const s = o - t, n = h - e;
                    i += Math.sqrt(s * s + n * n)
                }
                t = o, e = h
            }
            return i
        }

        point(t, e, i, s, n) {
            return e * (1 - t) * (1 - t) * (1 - t) + 3 * i * (1 - t) * (1 - t) * t + 3 * s * (1 - t) * t * t + n * t * t * t
        }
    }

    class i {
        constructor() {
            try {
                this._et = new EventTarget
            } catch (t) {
                this._et = document
            }
        }

        addEventListener(t, e, i) {
            this._et.addEventListener(t, e, i)
        }

        dispatchEvent(t) {
            return this._et.dispatchEvent(t)
        }

        removeEventListener(t, e, i) {
            this._et.removeEventListener(t, e, i)
        }
    }

    class s extends i {
        constructor(t, e = {}) {
            super(), this.canvas = t, this._drawningStroke = !1, this._isEmpty = !0, this._lastPoints = [], this._data = [], this._lastVelocity = 0, this._lastWidth = 0, this._handleMouseDown = t => {
                1 === t.buttons && (this._drawningStroke = !0, this._strokeBegin(t))
            }, this._handleMouseMove = t => {
                this._drawningStroke && this._strokeMoveUpdate(t)
            }, this._handleMouseUp = t => {
                1 === t.buttons && this._drawningStroke && (this._drawningStroke = !1, this._strokeEnd(t))
            }, this._handleTouchStart = t => {
                if (t.cancelable && t.preventDefault(), 1 === t.targetTouches.length) {
                    const e = t.changedTouches[0];
                    this._strokeBegin(e)
                }
            }, this._handleTouchMove = t => {
                t.cancelable && t.preventDefault();
                const e = t.targetTouches[0];
                this._strokeMoveUpdate(e)
            }, this._handleTouchEnd = t => {
                if (t.target === this.canvas) {
                    t.cancelable && t.preventDefault();
                    const e = t.changedTouches[0];
                    this._strokeEnd(e)
                }
            }, this._handlePointerStart = t => {
                this._drawningStroke = !0, t.preventDefault(), this._strokeBegin(t)
            }, this._handlePointerMove = t => {
                this._drawningStroke && (t.preventDefault(), this._strokeMoveUpdate(t))
            }, this._handlePointerEnd = t => {
                this._drawningStroke && (t.preventDefault(), this._drawningStroke = !1, this._strokeEnd(t))
            }, this.velocityFilterWeight = e.velocityFilterWeight || .7, this.minWidth = e.minWidth || .5, this.maxWidth = e.maxWidth || 2.5, this.throttle = "throttle" in e ? e.throttle : 16, this.minDistance = "minDistance" in e ? e.minDistance : 5, this.dotSize = e.dotSize || 0, this.penColor = e.penColor || "black", this.backgroundColor = e.backgroundColor || "rgba(0,0,0,0)", this._strokeMoveUpdate = this.throttle ? function (t, e = 250) {
                let i, s, n, o = 0, h = null;
                const r = () => {
                    o = Date.now(), h = null, i = t.apply(s, n), h || (s = null, n = [])
                };
                return function (...a) {
                    const d = Date.now(), c = e - (d - o);
                    return s = this, n = a, c <= 0 || c > e ? (h && (clearTimeout(h), h = null), o = d, i = t.apply(s, n), h || (s = null, n = [])) : h || (h = window.setTimeout(r, c)), i
                }
            }(s.prototype._strokeUpdate, this.throttle) : s.prototype._strokeUpdate, this._ctx = t.getContext("2d"), this.clear(), this.on()
        }

        clear() {
            const {_ctx: t, canvas: e} = this;
            t.fillStyle = this.backgroundColor, t.clearRect(0, 0, e.width, e.height), t.fillRect(0, 0, e.width, e.height), this._data = [], this._reset(this._getPointGroupOptions()), this._isEmpty = !0
        }

        fromDataURL(t, e = {}) {
            return new Promise(((i, s) => {
                const n = new Image, o = e.ratio || window.devicePixelRatio || 1, h = e.width || this.canvas.width / o,
                    r = e.height || this.canvas.height / o, a = e.xOffset || 0, d = e.yOffset || 0;
                this._reset(this._getPointGroupOptions()), n.onload = () => {
                    this._ctx.drawImage(n, a, d, h, r), i()
                }, n.onerror = t => {
                    s(t)
                }, n.crossOrigin = "anonymous", n.src = t, this._isEmpty = !1
            }))
        }

        toDataURL(t = "image/png", e) {
            return "image/svg+xml" === t ? ("object" != typeof e && (e = void 0), `data:image/svg+xml;base64,${btoa(this.toSVG(e))}`) : ("number" != typeof e && (e = void 0), this.canvas.toDataURL(t, e))
        }

        on() {
            this.canvas.style.touchAction = "none", this.canvas.style.msTouchAction = "none", this.canvas.style.userSelect = "none";
            const t = /Macintosh/.test(navigator.userAgent) && "ontouchstart" in document;
            window.PointerEvent && !t ? this._handlePointerEvents() : (this._handleMouseEvents(), "ontouchstart" in window && this._handleTouchEvents())
        }

        off() {
            this.canvas.style.touchAction = "auto", this.canvas.style.msTouchAction = "auto", this.canvas.style.userSelect = "auto", this.canvas.removeEventListener("pointerdown", this._handlePointerStart), this.canvas.removeEventListener("pointermove", this._handlePointerMove), this.canvas.ownerDocument.removeEventListener("pointerup", this._handlePointerEnd), this.canvas.removeEventListener("mousedown", this._handleMouseDown), this.canvas.removeEventListener("mousemove", this._handleMouseMove), this.canvas.ownerDocument.removeEventListener("mouseup", this._handleMouseUp), this.canvas.removeEventListener("touchstart", this._handleTouchStart), this.canvas.removeEventListener("touchmove", this._handleTouchMove), this.canvas.removeEventListener("touchend", this._handleTouchEnd)
        }

        isEmpty() {
            return this._isEmpty
        }

        fromData(t, {clear: e = !0} = {}) {
            e && this.clear(), this._fromData(t, this._drawCurve.bind(this), this._drawDot.bind(this)), this._data = this._data.concat(t)
        }

        toData() {
            return this._data
        }

        _getPointGroupOptions(t) {
            return {
                penColor: t && "penColor" in t ? t.penColor : this.penColor,
                dotSize: t && "dotSize" in t ? t.dotSize : this.dotSize,
                minWidth: t && "minWidth" in t ? t.minWidth : this.minWidth,
                maxWidth: t && "maxWidth" in t ? t.maxWidth : this.maxWidth,
                velocityFilterWeight: t && "velocityFilterWeight" in t ? t.velocityFilterWeight : this.velocityFilterWeight
            }
        }

        _strokeBegin(t) {
            this.dispatchEvent(new CustomEvent("beginStroke", {detail: t}));
            const e = this._getPointGroupOptions(), i = Object.assign(Object.assign({}, e), {points: []});
            this._data.push(i), this._reset(e), this._strokeUpdate(t)
        }

        _strokeUpdate(t) {
            if (0 === this._data.length) return void this._strokeBegin(t);
            this.dispatchEvent(new CustomEvent("beforeUpdateStroke", {detail: t}));
            const e = t.clientX, i = t.clientY,
                s = void 0 !== t.pressure ? t.pressure : void 0 !== t.force ? t.force : 0,
                n = this._createPoint(e, i, s), o = this._data[this._data.length - 1], h = o.points,
                r = h.length > 0 && h[h.length - 1], a = !!r && n.distanceTo(r) <= this.minDistance,
                d = this._getPointGroupOptions(o);
            if (!r || !r || !a) {
                const t = this._addPoint(n, d);
                r ? t && this._drawCurve(t, d) : this._drawDot(n, d), h.push({
                    time: n.time,
                    x: n.x,
                    y: n.y,
                    pressure: n.pressure
                })
            }
            this.dispatchEvent(new CustomEvent("afterUpdateStroke", {detail: t}))
        }

        _strokeEnd(t) {
            this._strokeUpdate(t), this.dispatchEvent(new CustomEvent("endStroke", {detail: t}))
        }

        _handlePointerEvents() {
            this._drawningStroke = !1, this.canvas.addEventListener("pointerdown", this._handlePointerStart), this.canvas.addEventListener("pointermove", this._handlePointerMove), this.canvas.ownerDocument.addEventListener("pointerup", this._handlePointerEnd)
        }

        _handleMouseEvents() {
            this._drawningStroke = !1, this.canvas.addEventListener("mousedown", this._handleMouseDown), this.canvas.addEventListener("mousemove", this._handleMouseMove), this.canvas.ownerDocument.addEventListener("mouseup", this._handleMouseUp)
        }

        _handleTouchEvents() {
            this.canvas.addEventListener("touchstart", this._handleTouchStart), this.canvas.addEventListener("touchmove", this._handleTouchMove), this.canvas.addEventListener("touchend", this._handleTouchEnd)
        }

        _reset(t) {
            this._lastPoints = [], this._lastVelocity = 0, this._lastWidth = (t.minWidth + t.maxWidth) / 2, this._ctx.fillStyle = t.penColor
        }

        _createPoint(e, i, s) {
            const n = this.canvas.getBoundingClientRect();
            return new t(e - n.left, i - n.top, s, (new Date).getTime())
        }

        _addPoint(t, i) {
            const {_lastPoints: s} = this;
            if (s.push(t), s.length > 2) {
                3 === s.length && s.unshift(s[0]);
                const t = this._calculateCurveWidths(s[1], s[2], i), n = e.fromPoints(s, t);
                return s.shift(), n
            }
            return null
        }

        _calculateCurveWidths(t, e, i) {
            const s = i.velocityFilterWeight * e.velocityFrom(t) + (1 - i.velocityFilterWeight) * this._lastVelocity,
                n = this._strokeWidth(s, i), o = {end: n, start: this._lastWidth};
            return this._lastVelocity = s, this._lastWidth = n, o
        }

        _strokeWidth(t, e) {
            return Math.max(e.maxWidth / (t + 1), e.minWidth)
        }

        _drawCurveSegment(t, e, i) {
            const s = this._ctx;
            s.moveTo(t, e), s.arc(t, e, i, 0, 2 * Math.PI, !1), this._isEmpty = !1
        }

        _drawCurve(t, e) {
            const i = this._ctx, s = t.endWidth - t.startWidth, n = 2 * Math.ceil(t.length());
            i.beginPath(), i.fillStyle = e.penColor;
            for (let i = 0; i < n; i += 1) {
                const o = i / n, h = o * o, r = h * o, a = 1 - o, d = a * a, c = d * a;
                let l = c * t.startPoint.x;
                l += 3 * d * o * t.control1.x, l += 3 * a * h * t.control2.x, l += r * t.endPoint.x;
                let u = c * t.startPoint.y;
                u += 3 * d * o * t.control1.y, u += 3 * a * h * t.control2.y, u += r * t.endPoint.y;
                const v = Math.min(t.startWidth + r * s, e.maxWidth);
                this._drawCurveSegment(l, u, v)
            }
            i.closePath(), i.fill()
        }

        _drawDot(t, e) {
            const i = this._ctx, s = e.dotSize > 0 ? e.dotSize : (e.minWidth + e.maxWidth) / 2;
            i.beginPath(), this._drawCurveSegment(t.x, t.y, s), i.closePath(), i.fillStyle = e.penColor, i.fill()
        }

        _fromData(e, i, s) {
            for (const n of e) {
                const {points: e} = n, o = this._getPointGroupOptions(n);
                if (e.length > 1) for (let s = 0; s < e.length; s += 1) {
                    const n = e[s], h = new t(n.x, n.y, n.pressure, n.time);
                    0 === s && this._reset(o);
                    const r = this._addPoint(h, o);
                    r && i(r, o)
                } else this._reset(o), s(e[0], o)
            }
        }

        toSVG({includeBackgroundColor: t = !1} = {}) {
            const e = this._data, i = Math.max(window.devicePixelRatio || 1, 1), s = this.canvas.width / i,
                n = this.canvas.height / i, o = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            if (o.setAttribute("xmlns", "http://www.w3.org/2000/svg"), o.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink"), o.setAttribute("viewBox", `0 0 ${s} ${n}`), o.setAttribute("width", s.toString()), o.setAttribute("height", n.toString()), t && this.backgroundColor) {
                const t = document.createElement("rect");
                t.setAttribute("width", "100%"), t.setAttribute("height", "100%"), t.setAttribute("fill", this.backgroundColor), o.appendChild(t)
            }
            return this._fromData(e, ((t, {penColor: e}) => {
                const i = document.createElement("path");
                if (!(isNaN(t.control1.x) || isNaN(t.control1.y) || isNaN(t.control2.x) || isNaN(t.control2.y))) {
                    const s = `M ${t.startPoint.x.toFixed(3)},${t.startPoint.y.toFixed(3)} C ${t.control1.x.toFixed(3)},${t.control1.y.toFixed(3)} ${t.control2.x.toFixed(3)},${t.control2.y.toFixed(3)} ${t.endPoint.x.toFixed(3)},${t.endPoint.y.toFixed(3)}`;
                    i.setAttribute("d", s), i.setAttribute("stroke-width", (2.25 * t.endWidth).toFixed(3)), i.setAttribute("stroke", e), i.setAttribute("fill", "none"), i.setAttribute("stroke-linecap", "round"), o.appendChild(i)
                }
            }), ((t, {penColor: e, dotSize: i, minWidth: s, maxWidth: n}) => {
                const h = document.createElement("circle"), r = i > 0 ? i : (s + n) / 2;
                h.setAttribute("r", r.toString()), h.setAttribute("cx", t.x.toString()), h.setAttribute("cy", t.y.toString()), h.setAttribute("fill", e), o.appendChild(h)
            })), o.outerHTML
        }
    }

    return s
}));

//# sourceMappingURL=signature_pad.umd.min.js.map
class FormExtDisableSectionCheckbox {
    constructor() {
        $(":checkbox.disableSectionCheckbox").change(evt => {
            const container = this.#toggleDisabledStateForInputsInsideSection(evt.currentTarget);
            container.find(":input:not(*[type='button']):disabled").val("");
        });
        $(":checkbox.disableSectionCheckbox").change();
    }

    #toggleDisabledStateForInputsInsideSection(chkDisabler) {

        const container = $(chkDisabler).closest("div:has(:header)");
        var disable = $(chkDisabler).hasClass("reversed") ? !chkDisabler.checked : chkDisabler.checked;
        var chkDisablerId = chkDisabler.id.split("_")[3],
            selectorDisabler = `[id*='${chkDisablerId}']`;
        var $inputs = container.find(`:input:not([name$='.ItemId']):not([name$='.Required']):not([id*='_Fields_Index_']):not(${selectorDisabler})`).prop("disabled", disable);

        var $inputIds = container.find(`:input[name$='.ItemId']:not(${selectorDisabler})`); // all hidden inputs containing IDs
        $inputIds.each(function () {
            var $inputId = $(this),
                id = $inputId.attr('id').split("_")[3],
                name = $inputId.attr('name'),
                nameRequired = name.replace('.ItemId', '.Required');
            $inputId.val(id); // in case if erased by other codePointAt

            // Special input that disables required condition
            var $required = container.find(`[name='${nameRequired}']`).val('false');
            if (!$required.length) {
                $required = $(`<input type='hidden' name='${nameRequired}' data-sc-conditions-required value="false" />`).insertAfter($inputId);
            }
            $required.attr('disabled', !disable); // inverse: disable when no need to disable Required, to not send .Required=false with form if 
        });

        var $chkHidden = $(`input[type='hidden'][name='${chkDisabler.name}']`) // hidden input that is supposed to contain checkbox value
            .val(disable ? 'true' : 'false'); // synchronise real value

        return container;
    }
}

class FormExtEnhancementWrapper {
    constructor() {
        for (const c of $(".enhanced-textbox .comment-tooltip").toArray()) {
            this.#initPopover(c);
        }
        try {
            if ($(".enhanced-textbox input[type='date']").prop("type") != "date") {
                $(".enhanced-textbox input[type='date']").datepicker();
            }
        } catch (err) {
            console.log("Datepicker plugin is absent");
        }
    }

    #initPopover(commentTooltip) {
        let isShown = false, resizing = false;
        const $commentTooltip = $(commentTooltip);
        const opts = {
            html: true,
            placement: "left",
            trigger: "manual",
            sanitize: false
        };
        if (!$commentTooltip.data("popover-init")) {
            $commentTooltip.data("popover-init", true);
            $commentTooltip.popover(opts);
        }
        else {
            return;
        }
        
        $commentTooltip.on("shown.bs.popover", function () {
            isShown = true;
            resizing = false;
        });
        $commentTooltip.on("hidden.bs.popover", function () {
            if (resizing) {
                $commentTooltip.popover("show");
            } else {
                isShown = false;
            }
        });
        $(window).resize(function () {
            if (isShown && !resizing) {
                resizing = true;
                $commentTooltip.popover("hide");
            }
        });
        $(document).mouseup(function (e) {
            const container = $(".popover:visible");
            if (isShown && !container.is(e.target) && !$commentTooltip.is(e.target) && container.has(e.target).length === 0) {
                $commentTooltip.popover("hide");
            }
        });
        $commentTooltip.click(evt => {
            $commentTooltip.popover("toggle");
        });
    }
}

class FormExtHiddenSectionToggle {
    constructor() {
        for (const addBtn of $("input.add-section").toArray()) {
            this.#initItem(addBtn);
        }
    }

    #hideOrShowAddBtnIfNeeded($addBtn, $sections) {
        $addBtn.toggle($sections.filter(":hidden").length > 0);
    };

    #toggleInputsDisableState(section, disable) {
        // $(section).find(":input").prop("disabled", disable);
        $(section).find(`:input:not([name$='.ItemId']):not([name$='.Required']):not([id*='_Fields_Index_'])`).prop("disabled", disable);

        var $inputIds = $(section).find(`:input[name$='.ItemId']`); // all hidden inputs containing IDs
        $inputIds.each(function () {
            var $inputId = $(this),
                id = $inputId.attr('id').split("_")[3],
                name = $inputId.attr('name'),
                nameRequired = name.replace('.ItemId', '.Required');
            var $required = $(section).find(`[name='${nameRequired}']`).val('false');
            if (!$required.length) {
                $required = $(`<input type='hidden' name='${nameRequired}' data-sc-conditions-required value="false" />`).insertAfter($inputId);
            }
            $required.attr('disabled', !disable); // inverse: disable when no need to disable Required, to not send .Required=false with form if 
        });
    };

    #saveSectionArrayToInput($serverDataInput, serverDataArr) {
        $serverDataInput.val(JSON.stringify(serverDataArr));
    };

    #toggleSectionInArray($serverDataInput, serverDataArr, index, val) {
        serverDataArr[index] = val;
        this.#saveSectionArrayToInput($serverDataInput, serverDataArr);
    };

    #initItem(addBtn) {
        const $addBtn = $(addBtn);
        const $sections = $("." + $addBtn.data("target-section-class"));
        const $serverDataInput = $addBtn.next("input").first();
        const serverData = $serverDataInput.val();
        let serverDataArr;
        if (serverData) {
            serverDataArr = JSON.parse(serverData);
        } else {
            serverDataArr = new Array($sections.length);
            serverDataArr[0] = true;
        }

        for (let i = 0; i < $sections.length; i++) {
            const $val = $($sections[i]);
            $val.data("index", i);
            if (i > 0) {
                $val.append(`<div class='${$addBtn.data("remove-button-container-class")}'><input type='button' class='${$addBtn.data("class")} ${$addBtn.data("remove-button-unique-class")}' value='${$addBtn.data("remove-button-label")}'/></div>`);
            }
            if (serverDataArr[i] !== true) {
                $val.hide();
                this.#toggleInputsDisableState($val, true);
                serverDataArr[i] = false;
            } else {
                $val.show();
                this.#toggleInputsDisableState($val, false);
            }
            $val.removeClass("hidden");
        }
        this.#saveSectionArrayToInput($serverDataInput, serverDataArr);

        $(`input.${$addBtn.data("remove-button-unique-class")}`).click(evt => {
            const $section = $(evt.currentTarget).closest(`div.${$addBtn.data("target-section-class")}`);
            $section.hide().find("input[type='text']").val("");
            this.#toggleInputsDisableState($section, true);
            $section.find("input[type='radio'], input[type='checkbox']").prop("checked", false);
            this.#hideOrShowAddBtnIfNeeded($addBtn, $sections);
            this.#toggleSectionInArray($serverDataInput, serverDataArr, $section.data("index"), false);
        });

        $addBtn.click(evt => {
            let $section = $sections.filter(":hidden:first");
            $section.show();
            this.#toggleInputsDisableState($section, false);
            this.#hideOrShowAddBtnIfNeeded($addBtn, $sections);
            this.#toggleSectionInArray($serverDataInput, serverDataArr, $section.data("index"), true);
        });

        this.#hideOrShowAddBtnIfNeeded($addBtn, $sections);
    }
}

class FormExtSignature {
    constructor() {
        for (const sig of $(".sigPad").toArray()) {
            const $signaturePadContainer = $(sig);
            const canvas = $signaturePadContainer.find("canvas")[0];
            const $dataField = $signaturePadContainer.find(".signature-image-data:first");
            const signaturePad = new SignaturePad(canvas);
            signaturePad.addEventListener("endStroke", () => {
                let imageData = signaturePad.toDataURL();
                imageData = imageData.substring(imageData.indexOf(",") + 1);
                $dataField.val(signaturePad.isEmpty() ? "" : imageData);
            });

            $signaturePadContainer.find(".clear").click(evt => {
                $dataField.val("");
                signaturePad.clear();
            });

            const $modal = $signaturePadContainer.closest("div.modal[role=dialog]");
            if ($modal.length && $modal.is(":hidden")) {
                $modal.on("shown.bs.modal", evt => {
                    this.#resizeCanvas(canvas, signaturePad);
                });
            } else {
                this.#resizeCanvas(canvas, signaturePad);
            }
            window.addEventListener("resize", () => this.#resizeCanvas(canvas, signaturePad));
        }
    }

    #resizeCanvas(canvas, signaturePad) {
        setTimeout(function () {
            const ratio = Math.max(window.devicePixelRatio || 1, 1);
            canvas.width = canvas.offsetWidth * ratio;
            canvas.height = canvas.offsetHeight * ratio;
            canvas.getContext("2d").scale(ratio, ratio);
            signaturePad.fromData(signaturePad.toData());
        }, 500);
    }
};
window.helperFunctions = {
    exists: function (el) {
        return el.length > 0;
    },
    isNumeric: function (num) {
        return /^\d+$/.test(num);
    },
    isIE8: function () {
        return $('.ie8').length > 0;
    }
};

function submitCategoriesSub(parentListId, uid, btn, evt, successMsg, categoriesError, constantGroupId) {
    var $dialog = $(btn).closest(".sub-blocks-email-form");
    if ($dialog.data("all") === "true") {
        uid = "";
    }
    var $loader = $dialog.find(".updateProgressDiv");
    var $email = $dialog.find("input[name='email']");
    if (!$email[0].checkValidity()) {
        $email.addClass("error");
        var $error = $email.siblings(".field-validation-error");
        if ($error.length === 0) {
            $error = $dialog.find(".field-validation-error");
        }
        $error.show();
        return false;
    }
    $email.removeClass("error");
    $dialog.find(".field-validation-error").hide();
    var uri = "/api/admin/SubscriptionCenter/ToggleGroupsAndList?listId=" + parentListId + "&email=" + $email.val();
    if (uid.length) {
        var categoriesContainer = $("#q" + parentListId + uid);
        if (categoriesContainer.length) {
            var categories = categoriesContainer.find("input:checked");
            if (categories.length === 0) {
                alert(categoriesError ?? "Please select one or more categories.");
                return false;
            }
            categories.each((i, el) => uri += "&groupId=" + $(el).data("group-id"));
        }
    }
    if (constantGroupId) {
        uri += "&groupId=" + constantGroupId;
    }
    $loader.show();
    $dialog.find("input").prop("disabled", true);
    $dialog.find("*[type=submit]").hide();
    $.get(uri)
        .done(data => {
            $dialog.find(".sub-blocks-messages").empty().append($("<div>" + successMsg + "</div>"));
        })
        .fail(() => {
            $dialog.find("input").prop("disabled", false);
            $dialog.find("*[type=submit]").show();
            alert("Server error occured. Please try again later.");
        })
        .always(() => $loader.hide());
    evt.preventDefault();
    return false;
};
class BaaqmdSessionManager {
    static #formRenderUrl = "/sitecore/content/DotGov/Home/Utils/FormRender?skipcache=1&id=";
    static #baseLink = '/admin/session/populate?skipcache=1';
    static #hasSession = false;

    static init() {
        const $allForms = $('form[data-sc-fxb]');
        if ($allForms.length) {
            $.get(this.#baseLink, function (data) {
                BaaqmdSessionManager.#hasSession = true;
                if (data.IsNewSession)
                    BaaqmdSessionManager.repopulateInlineForms($allForms);
            });
        }
    }

    static repopulateInlineForms($allForms) {
        $allForms.each((i, el) => {
            const $form = $(el);
            const $formId = $form.find('input[name$="FormItemId"]');
            if ($formId.length) {
                $.get(BaaqmdSessionManager.#formRenderUrl + $formId.val(), function (data) {
                    const $newForm = $(data);
                    $form.replaceWith($newForm);
                    eval($newForm.data("ajax-success"));
                });
            }
        });
    }

    static sessionPopulate(callback) {
        if (!BaaqmdSessionManager.#hasSession) {
            $.get(BaaqmdSessionManager.#baseLink, function (data) {
                BaaqmdSessionManager.#hasSession = true;
                callback(BaaqmdSessionManager.#formRenderUrl);
            });
        } else
            callback(BaaqmdSessionManager.#formRenderUrl);
    }
}

$(() => BaaqmdSessionManager.init());;
!function(t,e,i){!function(){var s,a,n,h="2.2.3",o="datepicker",r=".datepicker-here",c=!1,d='<div class="datepicker"><i class="datepicker--pointer"></i><nav class="datepicker--nav"></nav><div class="datepicker--content"></div></div>',l={classes:"",inline:!1,language:"ru",startDate:new Date,firstDay:"",weekends:[6,0],dateFormat:"",altField:"",altFieldDateFormat:"@",toggleSelected:!0,keyboardNav:!0,position:"bottom left",offset:12,view:"days",minView:"days",showOtherMonths:!0,selectOtherMonths:!0,moveToOtherMonthsOnSelect:!0,showOtherYears:!0,selectOtherYears:!0,moveToOtherYearsOnSelect:!0,minDate:"",maxDate:"",disableNavWhenOutOfRange:!0,multipleDates:!1,multipleDatesSeparator:",",range:!1,todayButton:!1,clearButton:!1,showEvent:"focus",autoClose:!1,monthsField:"monthsShort",prevHtml:'<svg><path d="M 17,12 l -5,5 l 5,5"></path></svg>',nextHtml:'<svg><path d="M 14,12 l 5,5 l -5,5"></path></svg>',navTitles:{days:"MM, <i>yyyy</i>",months:"yyyy",years:"yyyy1 - yyyy2"},timepicker:!1,onlyTimepicker:!1,dateTimeSeparator:" ",timeFormat:"",minHours:0,maxHours:24,minMinutes:0,maxMinutes:59,hoursStep:1,minutesStep:1,onSelect:"",onShow:"",onHide:"",onChangeMonth:"",onChangeYear:"",onChangeDecade:"",onChangeView:"",onRenderCell:""},u={ctrlRight:[17,39],ctrlUp:[17,38],ctrlLeft:[17,37],ctrlDown:[17,40],shiftRight:[16,39],shiftUp:[16,38],shiftLeft:[16,37],shiftDown:[16,40],altUp:[18,38],altRight:[18,39],altLeft:[18,37],altDown:[18,40],ctrlShiftUp:[16,17,38]},m=function(t,a){this.el=t,this.$el=e(t),this.opts=e.extend(!0,{},l,a,this.$el.data()),s==i&&(s=e("body")),this.opts.startDate||(this.opts.startDate=new Date),"INPUT"==this.el.nodeName&&(this.elIsInput=!0),this.opts.altField&&(this.$altField="string"==typeof this.opts.altField?e(this.opts.altField):this.opts.altField),this.inited=!1,this.visible=!1,this.silent=!1,this.currentDate=this.opts.startDate,this.currentView=this.opts.view,this._createShortCuts(),this.selectedDates=[],this.views={},this.keys=[],this.minRange="",this.maxRange="",this._prevOnSelectValue="",this.init()};n=m,n.prototype={VERSION:h,viewIndexes:["days","months","years"],init:function(){c||this.opts.inline||!this.elIsInput||this._buildDatepickersContainer(),this._buildBaseHtml(),this._defineLocale(this.opts.language),this._syncWithMinMaxDates(),this.elIsInput&&(this.opts.inline||(this._setPositionClasses(this.opts.position),this._bindEvents()),this.opts.keyboardNav&&!this.opts.onlyTimepicker&&this._bindKeyboardEvents(),this.$datepicker.on("mousedown",this._onMouseDownDatepicker.bind(this)),this.$datepicker.on("mouseup",this._onMouseUpDatepicker.bind(this))),this.opts.classes&&this.$datepicker.addClass(this.opts.classes),this.opts.timepicker&&(this.timepicker=new e.fn.datepicker.Timepicker(this,this.opts),this._bindTimepickerEvents()),this.opts.onlyTimepicker&&this.$datepicker.addClass("-only-timepicker-"),this.views[this.currentView]=new e.fn.datepicker.Body(this,this.currentView,this.opts),this.views[this.currentView].show(),this.nav=new e.fn.datepicker.Navigation(this,this.opts),this.view=this.currentView,this.$el.on("clickCell.adp",this._onClickCell.bind(this)),this.$datepicker.on("mouseenter",".datepicker--cell",this._onMouseEnterCell.bind(this)),this.$datepicker.on("mouseleave",".datepicker--cell",this._onMouseLeaveCell.bind(this)),this.inited=!0},_createShortCuts:function(){this.minDate=this.opts.minDate?this.opts.minDate:new Date(-86399999136e5),this.maxDate=this.opts.maxDate?this.opts.maxDate:new Date(86399999136e5)},_bindEvents:function(){this.$el.on(this.opts.showEvent+".adp",this._onShowEvent.bind(this)),this.$el.on("mouseup.adp",this._onMouseUpEl.bind(this)),this.$el.on("blur.adp",this._onBlur.bind(this)),this.$el.on("keyup.adp",this._onKeyUpGeneral.bind(this)),e(t).on("resize.adp",this._onResize.bind(this)),e("body").on("mouseup.adp",this._onMouseUpBody.bind(this))},_bindKeyboardEvents:function(){this.$el.on("keydown.adp",this._onKeyDown.bind(this)),this.$el.on("keyup.adp",this._onKeyUp.bind(this)),this.$el.on("hotKey.adp",this._onHotKey.bind(this))},_bindTimepickerEvents:function(){this.$el.on("timeChange.adp",this._onTimeChange.bind(this))},isWeekend:function(t){return-1!==this.opts.weekends.indexOf(t)},_defineLocale:function(t){"string"==typeof t?(this.loc=e.fn.datepicker.language[t],this.loc||(console.warn("Can't find language \""+t+'" in Datepicker.language, will use "ru" instead'),this.loc=e.extend(!0,{},e.fn.datepicker.language.ru)),this.loc=e.extend(!0,{},e.fn.datepicker.language.ru,e.fn.datepicker.language[t])):this.loc=e.extend(!0,{},e.fn.datepicker.language.ru,t),this.opts.dateFormat&&(this.loc.dateFormat=this.opts.dateFormat),this.opts.timeFormat&&(this.loc.timeFormat=this.opts.timeFormat),""!==this.opts.firstDay&&(this.loc.firstDay=this.opts.firstDay),this.opts.timepicker&&(this.loc.dateFormat=[this.loc.dateFormat,this.loc.timeFormat].join(this.opts.dateTimeSeparator)),this.opts.onlyTimepicker&&(this.loc.dateFormat=this.loc.timeFormat);var i=this._getWordBoundaryRegExp;(this.loc.timeFormat.match(i("aa"))||this.loc.timeFormat.match(i("AA")))&&(this.ampm=!0)},_buildDatepickersContainer:function(){c=!0,s.append('<div class="datepickers-container" id="datepickers-container"></div>'),a=e("#datepickers-container")},_buildBaseHtml:function(){var t,i=e('<div class="datepicker-inline">');t="INPUT"==this.el.nodeName?this.opts.inline?i.insertAfter(this.$el):a:i.appendTo(this.$el),this.$datepicker=e(d).appendTo(t),this.$content=e(".datepicker--content",this.$datepicker),this.$nav=e(".datepicker--nav",this.$datepicker)},_triggerOnChange:function(){if(!this.selectedDates.length){if(""===this._prevOnSelectValue)return;return this._prevOnSelectValue="",this.opts.onSelect("","",this)}var t,e=this.selectedDates,i=n.getParsedDate(e[0]),s=this,a=new Date(i.year,i.month,i.date,i.hours,i.minutes);t=e.map(function(t){return s.formatDate(s.loc.dateFormat,t)}).join(this.opts.multipleDatesSeparator),(this.opts.multipleDates||this.opts.range)&&(a=e.map(function(t){var e=n.getParsedDate(t);return new Date(e.year,e.month,e.date,e.hours,e.minutes)})),this._prevOnSelectValue=t,this.opts.onSelect(t,a,this)},next:function(){var t=this.parsedDate,e=this.opts;switch(this.view){case"days":this.date=new Date(t.year,t.month+1,1),e.onChangeMonth&&e.onChangeMonth(this.parsedDate.month,this.parsedDate.year);break;case"months":this.date=new Date(t.year+1,t.month,1),e.onChangeYear&&e.onChangeYear(this.parsedDate.year);break;case"years":this.date=new Date(t.year+10,0,1),e.onChangeDecade&&e.onChangeDecade(this.curDecade)}},prev:function(){var t=this.parsedDate,e=this.opts;switch(this.view){case"days":this.date=new Date(t.year,t.month-1,1),e.onChangeMonth&&e.onChangeMonth(this.parsedDate.month,this.parsedDate.year);break;case"months":this.date=new Date(t.year-1,t.month,1),e.onChangeYear&&e.onChangeYear(this.parsedDate.year);break;case"years":this.date=new Date(t.year-10,0,1),e.onChangeDecade&&e.onChangeDecade(this.curDecade)}},formatDate:function(t,e){e=e||this.date;var i,s=t,a=this._getWordBoundaryRegExp,h=this.loc,o=n.getLeadingZeroNum,r=n.getDecade(e),c=n.getParsedDate(e),d=c.fullHours,l=c.hours,u=t.match(a("aa"))||t.match(a("AA")),m="am",p=this._replacer;switch(this.opts.timepicker&&this.timepicker&&u&&(i=this.timepicker._getValidHoursFromDate(e,u),d=o(i.hours),l=i.hours,m=i.dayPeriod),!0){case/@/.test(s):s=s.replace(/@/,e.getTime());case/aa/.test(s):s=p(s,a("aa"),m);case/AA/.test(s):s=p(s,a("AA"),m.toUpperCase());case/dd/.test(s):s=p(s,a("dd"),c.fullDate);case/d/.test(s):s=p(s,a("d"),c.date);case/DD/.test(s):s=p(s,a("DD"),h.days[c.day]);case/D/.test(s):s=p(s,a("D"),h.daysShort[c.day]);case/mm/.test(s):s=p(s,a("mm"),c.fullMonth);case/m/.test(s):s=p(s,a("m"),c.month+1);case/MM/.test(s):s=p(s,a("MM"),this.loc.months[c.month]);case/M/.test(s):s=p(s,a("M"),h.monthsShort[c.month]);case/ii/.test(s):s=p(s,a("ii"),c.fullMinutes);case/i/.test(s):s=p(s,a("i"),c.minutes);case/hh/.test(s):s=p(s,a("hh"),d);case/h/.test(s):s=p(s,a("h"),l);case/yyyy/.test(s):s=p(s,a("yyyy"),c.year);case/yyyy1/.test(s):s=p(s,a("yyyy1"),r[0]);case/yyyy2/.test(s):s=p(s,a("yyyy2"),r[1]);case/yy/.test(s):s=p(s,a("yy"),c.year.toString().slice(-2))}return s},_replacer:function(t,e,i){return t.replace(e,function(t,e,s,a){return e+i+a})},_getWordBoundaryRegExp:function(t){var e="\\s|\\.|-|/|\\\\|,|\\$|\\!|\\?|:|;";return new RegExp("(^|>|"+e+")("+t+")($|<|"+e+")","g")},selectDate:function(t){var e=this,i=e.opts,s=e.parsedDate,a=e.selectedDates,h=a.length,o="";if(Array.isArray(t))return void t.forEach(function(t){e.selectDate(t)});if(t instanceof Date){if(this.lastSelectedDate=t,this.timepicker&&this.timepicker._setTime(t),e._trigger("selectDate",t),this.timepicker&&(t.setHours(this.timepicker.hours),t.setMinutes(this.timepicker.minutes)),"days"==e.view&&t.getMonth()!=s.month&&i.moveToOtherMonthsOnSelect&&(o=new Date(t.getFullYear(),t.getMonth(),1)),"years"==e.view&&t.getFullYear()!=s.year&&i.moveToOtherYearsOnSelect&&(o=new Date(t.getFullYear(),0,1)),o&&(e.silent=!0,e.date=o,e.silent=!1,e.nav._render()),i.multipleDates&&!i.range){if(h===i.multipleDates)return;e._isSelected(t)||e.selectedDates.push(t)}else i.range?2==h?(e.selectedDates=[t],e.minRange=t,e.maxRange=""):1==h?(e.selectedDates.push(t),e.maxRange?e.minRange=t:e.maxRange=t,n.bigger(e.maxRange,e.minRange)&&(e.maxRange=e.minRange,e.minRange=t),e.selectedDates=[e.minRange,e.maxRange]):(e.selectedDates=[t],e.minRange=t):e.selectedDates=[t];e._setInputValue(),i.onSelect&&e._triggerOnChange(),i.autoClose&&!this.timepickerIsActive&&(i.multipleDates||i.range?i.range&&2==e.selectedDates.length&&e.hide():e.hide()),e.views[this.currentView]._render()}},removeDate:function(t){var e=this.selectedDates,i=this;if(t instanceof Date)return e.some(function(s,a){return n.isSame(s,t)?(e.splice(a,1),i.selectedDates.length?i.lastSelectedDate=i.selectedDates[i.selectedDates.length-1]:(i.minRange="",i.maxRange="",i.lastSelectedDate=""),i.views[i.currentView]._render(),i._setInputValue(),i.opts.onSelect&&i._triggerOnChange(),!0):void 0})},today:function(){this.silent=!0,this.view=this.opts.minView,this.silent=!1,this.date=new Date,this.opts.todayButton instanceof Date&&this.selectDate(this.opts.todayButton)},clear:function(){this.selectedDates=[],this.minRange="",this.maxRange="",this.views[this.currentView]._render(),this._setInputValue(),this.opts.onSelect&&this._triggerOnChange()},update:function(t,i){var s=arguments.length,a=this.lastSelectedDate;return 2==s?this.opts[t]=i:1==s&&"object"==typeof t&&(this.opts=e.extend(!0,this.opts,t)),this._createShortCuts(),this._syncWithMinMaxDates(),this._defineLocale(this.opts.language),this.nav._addButtonsIfNeed(),this.opts.onlyTimepicker||this.nav._render(),this.views[this.currentView]._render(),this.elIsInput&&!this.opts.inline&&(this._setPositionClasses(this.opts.position),this.visible&&this.setPosition(this.opts.position)),this.opts.classes&&this.$datepicker.addClass(this.opts.classes),this.opts.onlyTimepicker&&this.$datepicker.addClass("-only-timepicker-"),this.opts.timepicker&&(a&&this.timepicker._handleDate(a),this.timepicker._updateRanges(),this.timepicker._updateCurrentTime(),a&&(a.setHours(this.timepicker.hours),a.setMinutes(this.timepicker.minutes))),this._setInputValue(),this},_syncWithMinMaxDates:function(){var t=this.date.getTime();this.silent=!0,this.minTime>t&&(this.date=this.minDate),this.maxTime<t&&(this.date=this.maxDate),this.silent=!1},_isSelected:function(t,e){var i=!1;return this.selectedDates.some(function(s){return n.isSame(s,t,e)?(i=s,!0):void 0}),i},_setInputValue:function(){var t,e=this,i=e.opts,s=e.loc.dateFormat,a=i.altFieldDateFormat,n=e.selectedDates.map(function(t){return e.formatDate(s,t)});i.altField&&e.$altField.length&&(t=this.selectedDates.map(function(t){return e.formatDate(a,t)}),t=t.join(this.opts.multipleDatesSeparator),this.$altField.val(t)),n=n.join(this.opts.multipleDatesSeparator),this.$el.val(n)},_isInRange:function(t,e){var i=t.getTime(),s=n.getParsedDate(t),a=n.getParsedDate(this.minDate),h=n.getParsedDate(this.maxDate),o=new Date(s.year,s.month,a.date).getTime(),r=new Date(s.year,s.month,h.date).getTime(),c={day:i>=this.minTime&&i<=this.maxTime,month:o>=this.minTime&&r<=this.maxTime,year:s.year>=a.year&&s.year<=h.year};return e?c[e]:c.day},_getDimensions:function(t){var e=t.offset();return{width:t.outerWidth(),height:t.outerHeight(),left:e.left,top:e.top}},_getDateFromCell:function(t){var e=this.parsedDate,s=t.data("year")||e.year,a=t.data("month")==i?e.month:t.data("month"),n=t.data("date")||1;return new Date(s,a,n)},_setPositionClasses:function(t){t=t.split(" ");var e=t[0],i=t[1],s="datepicker -"+e+"-"+i+"- -from-"+e+"-";this.visible&&(s+=" active"),this.$datepicker.removeAttr("class").addClass(s)},setPosition:function(t){t=t||this.opts.position;var e,i,s=this._getDimensions(this.$el),a=this._getDimensions(this.$datepicker),n=t.split(" "),h=this.opts.offset,o=n[0],r=n[1];switch(o){case"top":e=s.top-a.height-h;break;case"right":i=s.left+s.width+h;break;case"bottom":e=s.top+s.height+h;break;case"left":i=s.left-a.width-h}switch(r){case"top":e=s.top;break;case"right":i=s.left+s.width-a.width;break;case"bottom":e=s.top+s.height-a.height;break;case"left":i=s.left;break;case"center":/left|right/.test(o)?e=s.top+s.height/2-a.height/2:i=s.left+s.width/2-a.width/2}this.$datepicker.css({left:i,top:e})},show:function(){var t=this.opts.onShow;this.setPosition(this.opts.position),this.$datepicker.addClass("active"),this.visible=!0,t&&this._bindVisionEvents(t)},hide:function(){var t=this.opts.onHide;this.$datepicker.removeClass("active").css({left:"-100000px"}),this.focused="",this.keys=[],this.inFocus=!1,this.visible=!1,this.$el.blur(),t&&this._bindVisionEvents(t)},down:function(t){this._changeView(t,"down")},up:function(t){this._changeView(t,"up")},_bindVisionEvents:function(t){this.$datepicker.off("transitionend.dp"),t(this,!1),this.$datepicker.one("transitionend.dp",t.bind(this,this,!0))},_changeView:function(t,e){t=t||this.focused||this.date;var i="up"==e?this.viewIndex+1:this.viewIndex-1;i>2&&(i=2),0>i&&(i=0),this.silent=!0,this.date=new Date(t.getFullYear(),t.getMonth(),1),this.silent=!1,this.view=this.viewIndexes[i]},_handleHotKey:function(t){var e,i,s,a=n.getParsedDate(this._getFocusedDate()),h=this.opts,o=!1,r=!1,c=!1,d=a.year,l=a.month,u=a.date;switch(t){case"ctrlRight":case"ctrlUp":l+=1,o=!0;break;case"ctrlLeft":case"ctrlDown":l-=1,o=!0;break;case"shiftRight":case"shiftUp":r=!0,d+=1;break;case"shiftLeft":case"shiftDown":r=!0,d-=1;break;case"altRight":case"altUp":c=!0,d+=10;break;case"altLeft":case"altDown":c=!0,d-=10;break;case"ctrlShiftUp":this.up()}s=n.getDaysCount(new Date(d,l)),i=new Date(d,l,u),u>s&&(u=s),i.getTime()<this.minTime?i=this.minDate:i.getTime()>this.maxTime&&(i=this.maxDate),this.focused=i,e=n.getParsedDate(i),o&&h.onChangeMonth&&h.onChangeMonth(e.month,e.year),r&&h.onChangeYear&&h.onChangeYear(e.year),c&&h.onChangeDecade&&h.onChangeDecade(this.curDecade)},_registerKey:function(t){var e=this.keys.some(function(e){return e==t});e||this.keys.push(t)},_unRegisterKey:function(t){var e=this.keys.indexOf(t);this.keys.splice(e,1)},_isHotKeyPressed:function(){var t,e=!1,i=this,s=this.keys.sort();for(var a in u)t=u[a],s.length==t.length&&t.every(function(t,e){return t==s[e]})&&(i._trigger("hotKey",a),e=!0);return e},_trigger:function(t,e){this.$el.trigger(t,e)},_focusNextCell:function(t,e){e=e||this.cellType;var i=n.getParsedDate(this._getFocusedDate()),s=i.year,a=i.month,h=i.date;if(!this._isHotKeyPressed()){switch(t){case 37:"day"==e?h-=1:"","month"==e?a-=1:"","year"==e?s-=1:"";break;case 38:"day"==e?h-=7:"","month"==e?a-=3:"","year"==e?s-=4:"";break;case 39:"day"==e?h+=1:"","month"==e?a+=1:"","year"==e?s+=1:"";break;case 40:"day"==e?h+=7:"","month"==e?a+=3:"","year"==e?s+=4:""}var o=new Date(s,a,h);o.getTime()<this.minTime?o=this.minDate:o.getTime()>this.maxTime&&(o=this.maxDate),this.focused=o}},_getFocusedDate:function(){var t=this.focused||this.selectedDates[this.selectedDates.length-1],e=this.parsedDate;if(!t)switch(this.view){case"days":t=new Date(e.year,e.month,(new Date).getDate());break;case"months":t=new Date(e.year,e.month,1);break;case"years":t=new Date(e.year,0,1)}return t},_getCell:function(t,i){i=i||this.cellType;var s,a=n.getParsedDate(t),h='.datepicker--cell[data-year="'+a.year+'"]';switch(i){case"month":h='[data-month="'+a.month+'"]';break;case"day":h+='[data-month="'+a.month+'"][data-date="'+a.date+'"]'}return s=this.views[this.currentView].$el.find(h),s.length?s:e("")},destroy:function(){var t=this;t.$el.off(".adp").data("datepicker",""),t.selectedDates=[],t.focused="",t.views={},t.keys=[],t.minRange="",t.maxRange="",t.opts.inline||!t.elIsInput?t.$datepicker.closest(".datepicker-inline").remove():t.$datepicker.remove()},_handleAlreadySelectedDates:function(t,e){this.opts.range?this.opts.toggleSelected?this.removeDate(e):2!=this.selectedDates.length&&this._trigger("clickCell",e):this.opts.toggleSelected&&this.removeDate(e),this.opts.toggleSelected||(this.lastSelectedDate=t,this.opts.timepicker&&(this.timepicker._setTime(t),this.timepicker.update()))},_onShowEvent:function(t){this.visible||this.show()},_onBlur:function(){!this.inFocus&&this.visible&&this.hide()},_onMouseDownDatepicker:function(t){this.inFocus=!0},_onMouseUpDatepicker:function(t){this.inFocus=!1,t.originalEvent.inFocus=!0,t.originalEvent.timepickerFocus||this.$el.focus()},_onKeyUpGeneral:function(t){var e=this.$el.val();e||this.clear()},_onResize:function(){this.visible&&this.setPosition()},_onMouseUpBody:function(t){t.originalEvent.inFocus||this.visible&&!this.inFocus&&this.hide()},_onMouseUpEl:function(t){t.originalEvent.inFocus=!0,setTimeout(this._onKeyUpGeneral.bind(this),4)},_onKeyDown:function(t){var e=t.which;if(this._registerKey(e),e>=37&&40>=e&&(t.preventDefault(),this._focusNextCell(e)),13==e&&this.focused){if(this._getCell(this.focused).hasClass("-disabled-"))return;if(this.view!=this.opts.minView)this.down();else{var i=this._isSelected(this.focused,this.cellType);if(!i)return this.timepicker&&(this.focused.setHours(this.timepicker.hours),this.focused.setMinutes(this.timepicker.minutes)),void this.selectDate(this.focused);this._handleAlreadySelectedDates(i,this.focused)}}27==e&&this.hide()},_onKeyUp:function(t){var e=t.which;this._unRegisterKey(e)},_onHotKey:function(t,e){this._handleHotKey(e)},_onMouseEnterCell:function(t){var i=e(t.target).closest(".datepicker--cell"),s=this._getDateFromCell(i);this.silent=!0,this.focused&&(this.focused=""),i.addClass("-focus-"),this.focused=s,this.silent=!1,this.opts.range&&1==this.selectedDates.length&&(this.minRange=this.selectedDates[0],this.maxRange="",n.less(this.minRange,this.focused)&&(this.maxRange=this.minRange,this.minRange=""),this.views[this.currentView]._update())},_onMouseLeaveCell:function(t){var i=e(t.target).closest(".datepicker--cell");i.removeClass("-focus-"),this.silent=!0,this.focused="",this.silent=!1},_onTimeChange:function(t,e,i){var s=new Date,a=this.selectedDates,n=!1;a.length&&(n=!0,s=this.lastSelectedDate),s.setHours(e),s.setMinutes(i),n||this._getCell(s).hasClass("-disabled-")?(this._setInputValue(),this.opts.onSelect&&this._triggerOnChange()):this.selectDate(s)},_onClickCell:function(t,e){this.timepicker&&(e.setHours(this.timepicker.hours),e.setMinutes(this.timepicker.minutes)),this.selectDate(e)},set focused(t){if(!t&&this.focused){var e=this._getCell(this.focused);e.length&&e.removeClass("-focus-")}this._focused=t,this.opts.range&&1==this.selectedDates.length&&(this.minRange=this.selectedDates[0],this.maxRange="",n.less(this.minRange,this._focused)&&(this.maxRange=this.minRange,this.minRange="")),this.silent||(this.date=t)},get focused(){return this._focused},get parsedDate(){return n.getParsedDate(this.date)},set date(t){return t instanceof Date?(this.currentDate=t,this.inited&&!this.silent&&(this.views[this.view]._render(),this.nav._render(),this.visible&&this.elIsInput&&this.setPosition()),t):void 0},get date(){return this.currentDate},set view(t){return this.viewIndex=this.viewIndexes.indexOf(t),this.viewIndex<0?void 0:(this.prevView=this.currentView,this.currentView=t,this.inited&&(this.views[t]?this.views[t]._render():this.views[t]=new e.fn.datepicker.Body(this,t,this.opts),this.views[this.prevView].hide(),this.views[t].show(),this.nav._render(),this.opts.onChangeView&&this.opts.onChangeView(t),this.elIsInput&&this.visible&&this.setPosition()),t)},get view(){return this.currentView},get cellType(){return this.view.substring(0,this.view.length-1)},get minTime(){var t=n.getParsedDate(this.minDate);return new Date(t.year,t.month,t.date).getTime()},get maxTime(){var t=n.getParsedDate(this.maxDate);return new Date(t.year,t.month,t.date).getTime()},get curDecade(){return n.getDecade(this.date)}},n.getDaysCount=function(t){return new Date(t.getFullYear(),t.getMonth()+1,0).getDate()},n.getParsedDate=function(t){return{year:t.getFullYear(),month:t.getMonth(),fullMonth:t.getMonth()+1<10?"0"+(t.getMonth()+1):t.getMonth()+1,date:t.getDate(),fullDate:t.getDate()<10?"0"+t.getDate():t.getDate(),day:t.getDay(),hours:t.getHours(),fullHours:t.getHours()<10?"0"+t.getHours():t.getHours(),minutes:t.getMinutes(),fullMinutes:t.getMinutes()<10?"0"+t.getMinutes():t.getMinutes()}},n.getDecade=function(t){var e=10*Math.floor(t.getFullYear()/10);return[e,e+9]},n.template=function(t,e){return t.replace(/#\{([\w]+)\}/g,function(t,i){return e[i]||0===e[i]?e[i]:void 0})},n.isSame=function(t,e,i){if(!t||!e)return!1;var s=n.getParsedDate(t),a=n.getParsedDate(e),h=i?i:"day",o={day:s.date==a.date&&s.month==a.month&&s.year==a.year,month:s.month==a.month&&s.year==a.year,year:s.year==a.year};return o[h]},n.less=function(t,e,i){return t&&e?e.getTime()<t.getTime():!1},n.bigger=function(t,e,i){return t&&e?e.getTime()>t.getTime():!1},n.getLeadingZeroNum=function(t){return parseInt(t)<10?"0"+t:t},n.resetTime=function(t){return"object"==typeof t?(t=n.getParsedDate(t),new Date(t.year,t.month,t.date)):void 0},e.fn.datepicker=function(t){return this.each(function(){if(e.data(this,o)){var i=e.data(this,o);i.opts=e.extend(!0,i.opts,t),i.update()}else e.data(this,o,new m(this,t))})},e.fn.datepicker.Constructor=m,e.fn.datepicker.language={ru:{days:["Воскресенье","Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"],daysShort:["Вос","Пон","Вто","Сре","Чет","Пят","Суб"],daysMin:["Вс","Пн","Вт","Ср","Чт","Пт","Сб"],months:["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"],monthsShort:["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"],today:"Сегодня",clear:"Очистить",dateFormat:"dd.mm.yyyy",timeFormat:"hh:ii",firstDay:1}},e(function(){e(r).datepicker()})}(),function(){var t={days:'<div class="datepicker--days datepicker--body"><div class="datepicker--days-names"></div><div class="datepicker--cells datepicker--cells-days"></div></div>',months:'<div class="datepicker--months datepicker--body"><div class="datepicker--cells datepicker--cells-months"></div></div>',years:'<div class="datepicker--years datepicker--body"><div class="datepicker--cells datepicker--cells-years"></div></div>'},s=e.fn.datepicker,a=s.Constructor;s.Body=function(t,i,s){this.d=t,this.type=i,this.opts=s,this.$el=e(""),this.opts.onlyTimepicker||this.init()},s.Body.prototype={init:function(){this._buildBaseHtml(),this._render(),this._bindEvents()},_bindEvents:function(){this.$el.on("click",".datepicker--cell",e.proxy(this._onClickCell,this))},_buildBaseHtml:function(){this.$el=e(t[this.type]).appendTo(this.d.$content),this.$names=e(".datepicker--days-names",this.$el),this.$cells=e(".datepicker--cells",this.$el)},_getDayNamesHtml:function(t,e,s,a){return e=e!=i?e:t,s=s?s:"",a=a!=i?a:0,a>7?s:7==e?this._getDayNamesHtml(t,0,s,++a):(s+='<div class="datepicker--day-name'+(this.d.isWeekend(e)?" -weekend-":"")+'">'+this.d.loc.daysMin[e]+"</div>",this._getDayNamesHtml(t,++e,s,++a))},_getCellContents:function(t,e){var i="datepicker--cell datepicker--cell-"+e,s=new Date,n=this.d,h=a.resetTime(n.minRange),o=a.resetTime(n.maxRange),r=n.opts,c=a.getParsedDate(t),d={},l=c.date;switch(e){case"day":n.isWeekend(c.day)&&(i+=" -weekend-"),c.month!=this.d.parsedDate.month&&(i+=" -other-month-",r.selectOtherMonths||(i+=" -disabled-"),r.showOtherMonths||(l=""));break;case"month":l=n.loc[n.opts.monthsField][c.month];break;case"year":var u=n.curDecade;l=c.year,(c.year<u[0]||c.year>u[1])&&(i+=" -other-decade-",r.selectOtherYears||(i+=" -disabled-"),r.showOtherYears||(l=""))}return r.onRenderCell&&(d=r.onRenderCell(t,e)||{},l=d.html?d.html:l,i+=d.classes?" "+d.classes:""),r.range&&(a.isSame(h,t,e)&&(i+=" -range-from-"),a.isSame(o,t,e)&&(i+=" -range-to-"),1==n.selectedDates.length&&n.focused?((a.bigger(h,t)&&a.less(n.focused,t)||a.less(o,t)&&a.bigger(n.focused,t))&&(i+=" -in-range-"),a.less(o,t)&&a.isSame(n.focused,t)&&(i+=" -range-from-"),a.bigger(h,t)&&a.isSame(n.focused,t)&&(i+=" -range-to-")):2==n.selectedDates.length&&a.bigger(h,t)&&a.less(o,t)&&(i+=" -in-range-")),a.isSame(s,t,e)&&(i+=" -current-"),n.focused&&a.isSame(t,n.focused,e)&&(i+=" -focus-"),n._isSelected(t,e)&&(i+=" -selected-"),(!n._isInRange(t,e)||d.disabled)&&(i+=" -disabled-"),{html:l,classes:i}},_getDaysHtml:function(t){var e=a.getDaysCount(t),i=new Date(t.getFullYear(),t.getMonth(),1).getDay(),s=new Date(t.getFullYear(),t.getMonth(),e).getDay(),n=i-this.d.loc.firstDay,h=6-s+this.d.loc.firstDay;n=0>n?n+7:n,h=h>6?h-7:h;for(var o,r,c=-n+1,d="",l=c,u=e+h;u>=l;l++)r=t.getFullYear(),o=t.getMonth(),d+=this._getDayHtml(new Date(r,o,l));return d},_getDayHtml:function(t){var e=this._getCellContents(t,"day");return'<div class="'+e.classes+'" data-date="'+t.getDate()+'" data-month="'+t.getMonth()+'" data-year="'+t.getFullYear()+'">'+e.html+"</div>"},_getMonthsHtml:function(t){for(var e="",i=a.getParsedDate(t),s=0;12>s;)e+=this._getMonthHtml(new Date(i.year,s)),s++;return e},_getMonthHtml:function(t){var e=this._getCellContents(t,"month");return'<div class="'+e.classes+'" data-month="'+t.getMonth()+'">'+e.html+"</div>"},_getYearsHtml:function(t){var e=(a.getParsedDate(t),a.getDecade(t)),i=e[0]-1,s="",n=i;for(n;n<=e[1]+1;n++)s+=this._getYearHtml(new Date(n,0));return s},_getYearHtml:function(t){var e=this._getCellContents(t,"year");return'<div class="'+e.classes+'" data-year="'+t.getFullYear()+'">'+e.html+"</div>"},_renderTypes:{days:function(){var t=this._getDayNamesHtml(this.d.loc.firstDay),e=this._getDaysHtml(this.d.currentDate);this.$cells.html(e),this.$names.html(t)},months:function(){var t=this._getMonthsHtml(this.d.currentDate);this.$cells.html(t)},years:function(){var t=this._getYearsHtml(this.d.currentDate);this.$cells.html(t)}},_render:function(){this.opts.onlyTimepicker||this._renderTypes[this.type].bind(this)()},_update:function(){var t,i,s,a=e(".datepicker--cell",this.$cells),n=this;a.each(function(a,h){i=e(this),s=n.d._getDateFromCell(e(this)),t=n._getCellContents(s,n.d.cellType),i.attr("class",t.classes)})},show:function(){this.opts.onlyTimepicker||(this.$el.addClass("active"),this.acitve=!0)},hide:function(){this.$el.removeClass("active"),this.active=!1},_handleClick:function(t){var e=t.data("date")||1,i=t.data("month")||0,s=t.data("year")||this.d.parsedDate.year,a=this.d;if(a.view!=this.opts.minView)return void a.down(new Date(s,i,e));var n=new Date(s,i,e),h=this.d._isSelected(n,this.d.cellType);return h?void a._handleAlreadySelectedDates.bind(a,h,n)():void a._trigger("clickCell",n)},_onClickCell:function(t){var i=e(t.target).closest(".datepicker--cell");i.hasClass("-disabled-")||this._handleClick.bind(this)(i)}}}(),function(){var t='<div class="datepicker--nav-action" data-action="prev">#{prevHtml}</div><div class="datepicker--nav-title">#{title}</div><div class="datepicker--nav-action" data-action="next">#{nextHtml}</div>',i='<div class="datepicker--buttons"></div>',s='<span class="datepicker--button" data-action="#{action}">#{label}</span>',a=e.fn.datepicker,n=a.Constructor;a.Navigation=function(t,e){this.d=t,this.opts=e,this.$buttonsContainer="",this.init()},a.Navigation.prototype={init:function(){this._buildBaseHtml(),this._bindEvents()},_bindEvents:function(){this.d.$nav.on("click",".datepicker--nav-action",e.proxy(this._onClickNavButton,this)),this.d.$nav.on("click",".datepicker--nav-title",e.proxy(this._onClickNavTitle,this)),this.d.$datepicker.on("click",".datepicker--button",e.proxy(this._onClickNavButton,this))},_buildBaseHtml:function(){this.opts.onlyTimepicker||this._render(),this._addButtonsIfNeed()},_addButtonsIfNeed:function(){this.opts.todayButton&&this._addButton("today"),this.opts.clearButton&&this._addButton("clear")},_render:function(){var i=this._getTitle(this.d.currentDate),s=n.template(t,e.extend({title:i},this.opts));this.d.$nav.html(s),"years"==this.d.view&&e(".datepicker--nav-title",this.d.$nav).addClass("-disabled-"),this.setNavStatus()},_getTitle:function(t){return this.d.formatDate(this.opts.navTitles[this.d.view],t)},_addButton:function(t){this.$buttonsContainer.length||this._addButtonsContainer();var i={action:t,label:this.d.loc[t]},a=n.template(s,i);e("[data-action="+t+"]",this.$buttonsContainer).length||this.$buttonsContainer.append(a)},_addButtonsContainer:function(){this.d.$datepicker.append(i),this.$buttonsContainer=e(".datepicker--buttons",this.d.$datepicker)},setNavStatus:function(){if((this.opts.minDate||this.opts.maxDate)&&this.opts.disableNavWhenOutOfRange){var t=this.d.parsedDate,e=t.month,i=t.year,s=t.date;switch(this.d.view){case"days":this.d._isInRange(new Date(i,e-1,1),"month")||this._disableNav("prev"),this.d._isInRange(new Date(i,e+1,1),"month")||this._disableNav("next");break;case"months":this.d._isInRange(new Date(i-1,e,s),"year")||this._disableNav("prev"),this.d._isInRange(new Date(i+1,e,s),"year")||this._disableNav("next");break;case"years":var a=n.getDecade(this.d.date);this.d._isInRange(new Date(a[0]-1,0,1),"year")||this._disableNav("prev"),this.d._isInRange(new Date(a[1]+1,0,1),"year")||this._disableNav("next")}}},_disableNav:function(t){e('[data-action="'+t+'"]',this.d.$nav).addClass("-disabled-")},_activateNav:function(t){e('[data-action="'+t+'"]',this.d.$nav).removeClass("-disabled-")},_onClickNavButton:function(t){var i=e(t.target).closest("[data-action]"),s=i.data("action");this.d[s]()},_onClickNavTitle:function(t){return e(t.target).hasClass("-disabled-")?void 0:"days"==this.d.view?this.d.view="months":void(this.d.view="years")}}}(),function(){var t='<div class="datepicker--time"><div class="datepicker--time-current">   <span class="datepicker--time-current-hours">#{hourVisible}</span>   <span class="datepicker--time-current-colon">:</span>   <span class="datepicker--time-current-minutes">#{minValue}</span></div><div class="datepicker--time-sliders">   <div class="datepicker--time-row">      <input type="range" name="hours" value="#{hourValue}" min="#{hourMin}" max="#{hourMax}" step="#{hourStep}"/>   </div>   <div class="datepicker--time-row">      <input type="range" name="minutes" value="#{minValue}" min="#{minMin}" max="#{minMax}" step="#{minStep}"/>   </div></div></div>',i=e.fn.datepicker,s=i.Constructor;i.Timepicker=function(t,e){this.d=t,this.opts=e,this.init()},i.Timepicker.prototype={init:function(){var t="input";this._setTime(this.d.date),this._buildHTML(),navigator.userAgent.match(/trident/gi)&&(t="change"),this.d.$el.on("selectDate",this._onSelectDate.bind(this)),this.$ranges.on(t,this._onChangeRange.bind(this)),this.$ranges.on("mouseup",this._onMouseUpRange.bind(this)),this.$ranges.on("mousemove focus ",this._onMouseEnterRange.bind(this)),this.$ranges.on("mouseout blur",this._onMouseOutRange.bind(this))},_setTime:function(t){var e=s.getParsedDate(t);this._handleDate(t),this.hours=e.hours<this.minHours?this.minHours:e.hours,this.minutes=e.minutes<this.minMinutes?this.minMinutes:e.minutes},_setMinTimeFromDate:function(t){this.minHours=t.getHours(),this.minMinutes=t.getMinutes(),this.d.lastSelectedDate&&this.d.lastSelectedDate.getHours()>t.getHours()&&(this.minMinutes=this.opts.minMinutes)},_setMaxTimeFromDate:function(t){
        this.maxHours=t.getHours(),this.maxMinutes=t.getMinutes(),this.d.lastSelectedDate&&this.d.lastSelectedDate.getHours()<t.getHours()&&(this.maxMinutes=this.opts.maxMinutes)},_setDefaultMinMaxTime:function(){var t=23,e=59,i=this.opts;this.minHours=i.minHours<0||i.minHours>t?0:i.minHours,this.minMinutes=i.minMinutes<0||i.minMinutes>e?0:i.minMinutes,this.maxHours=i.maxHours<0||i.maxHours>t?t:i.maxHours,this.maxMinutes=i.maxMinutes<0||i.maxMinutes>e?e:i.maxMinutes},_validateHoursMinutes:function(t){this.hours<this.minHours?this.hours=this.minHours:this.hours>this.maxHours&&(this.hours=this.maxHours),this.minutes<this.minMinutes?this.minutes=this.minMinutes:this.minutes>this.maxMinutes&&(this.minutes=this.maxMinutes)},_buildHTML:function(){var i=s.getLeadingZeroNum,a={hourMin:this.minHours,hourMax:i(this.maxHours),hourStep:this.opts.hoursStep,hourValue:this.hours,hourVisible:i(this.displayHours),minMin:this.minMinutes,minMax:i(this.maxMinutes),minStep:this.opts.minutesStep,minValue:i(this.minutes)},n=s.template(t,a);this.$timepicker=e(n).appendTo(this.d.$datepicker),this.$ranges=e('[type="range"]',this.$timepicker),this.$hours=e('[name="hours"]',this.$timepicker),this.$minutes=e('[name="minutes"]',this.$timepicker),this.$hoursText=e(".datepicker--time-current-hours",this.$timepicker),this.$minutesText=e(".datepicker--time-current-minutes",this.$timepicker),this.d.ampm&&(this.$ampm=e('<span class="datepicker--time-current-ampm">').appendTo(e(".datepicker--time-current",this.$timepicker)).html(this.dayPeriod),this.$timepicker.addClass("-am-pm-"))},_updateCurrentTime:function(){var t=s.getLeadingZeroNum(this.displayHours),e=s.getLeadingZeroNum(this.minutes);this.$hoursText.html(t),this.$minutesText.html(e),this.d.ampm&&this.$ampm.html(this.dayPeriod)},_updateRanges:function(){this.$hours.attr({min:this.minHours,max:this.maxHours}).val(this.hours),this.$minutes.attr({min:this.minMinutes,max:this.maxMinutes}).val(this.minutes)},_handleDate:function(t){this._setDefaultMinMaxTime(),t&&(s.isSame(t,this.d.opts.minDate)?this._setMinTimeFromDate(this.d.opts.minDate):s.isSame(t,this.d.opts.maxDate)&&this._setMaxTimeFromDate(this.d.opts.maxDate)),this._validateHoursMinutes(t)},update:function(){this._updateRanges(),this._updateCurrentTime()},_getValidHoursFromDate:function(t,e){var i=t,a=t;t instanceof Date&&(i=s.getParsedDate(t),a=i.hours);var n=e||this.d.ampm,h="am";if(n)switch(!0){case 0==a:a=12;break;case 12==a:h="pm";break;case a>11:a-=12,h="pm"}return{hours:a,dayPeriod:h}},set hours(t){this._hours=t;var e=this._getValidHoursFromDate(t);this.displayHours=e.hours,this.dayPeriod=e.dayPeriod},get hours(){return this._hours},_onChangeRange:function(t){var i=e(t.target),s=i.attr("name");this.d.timepickerIsActive=!0,this[s]=i.val(),this._updateCurrentTime(),this.d._trigger("timeChange",[this.hours,this.minutes]),this._handleDate(this.d.lastSelectedDate),this.update()},_onSelectDate:function(t,e){this._handleDate(e),this.update()},_onMouseEnterRange:function(t){var i=e(t.target).attr("name");e(".datepicker--time-current-"+i,this.$timepicker).addClass("-focus-")},_onMouseOutRange:function(t){var i=e(t.target).attr("name");this.d.inFocus||e(".datepicker--time-current-"+i,this.$timepicker).removeClass("-focus-")},_onMouseUpRange:function(t){this.d.timepickerIsActive=!1}}}()}(window,jQuery);
!function(a){a.fn.datepicker.language.en={days:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],daysShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],daysMin:["Su","Mo","Tu","We","Th","Fr","Sa"],months:["January","February","March","April","May","June","July","August","September","October","November","December"],monthsShort:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],today:"Today",clear:"Clear",dateFormat:"mm/dd/yyyy",timeFormat:"hh:ii aa",firstDay:0}}(jQuery);
//# sourceMappingURL=datepicker.en.min.js.map;
!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?e(exports):"function"==typeof define&&define.amd?define(["exports"],e):e((t||self).gridjs={})}(this,function(t){function e(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}function n(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}function r(){return r=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var n=arguments[e];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(t[r]=n[r])}return t},r.apply(this,arguments)}function i(t,e){t.prototype=Object.create(e.prototype),t.prototype.constructor=t,o(t,e)}function o(t,e){return o=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},o(t,e)}function s(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}function a(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}function u(t,e){var n="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(n)return(n=n.call(t)).next.bind(n);if(Array.isArray(t)||(n=function(t,e){if(t){if("string"==typeof t)return a(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);return"Object"===n&&t.constructor&&(n=t.constructor.name),"Map"===n||"Set"===n?Array.from(t):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?a(t,e):void 0}}(t))||e&&t&&"number"==typeof t.length){n&&(t=n);var r=0;return function(){return r>=t.length?{done:!0}:{done:!1,value:t[r++]}}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var l,c,p,h,f,d,_,m={},g=[],v=/acit|ex(?:s|g|n|p|$)|rph|grid|ows|mnc|ntw|ine[ch]|zoo|^ord|itera/i;function y(t,e){for(var n in e)t[n]=e[n];return t}function b(t){var e=t.parentNode;e&&e.removeChild(t)}function w(t,e,n){var r,i,o,s={};for(o in e)"key"==o?r=e[o]:"ref"==o?i=e[o]:s[o]=e[o];if(arguments.length>2&&(s.children=arguments.length>3?l.call(arguments,2):n),"function"==typeof t&&null!=t.defaultProps)for(o in t.defaultProps)void 0===s[o]&&(s[o]=t.defaultProps[o]);return P(t,s,r,i,null)}function P(t,e,n,r,i){var o={type:t,props:e,key:n,ref:r,__k:null,__:null,__b:0,__e:null,__d:void 0,__c:null,__h:null,constructor:void 0,__v:null==i?++p:i};return null==i&&null!=c.vnode&&c.vnode(o),o}function S(t){return t.children}function k(t,e){this.props=t,this.context=e}function C(t,e){if(null==e)return t.__?C(t.__,t.__.__k.indexOf(t)+1):null;for(var n;e<t.__k.length;e++)if(null!=(n=t.__k[e])&&null!=n.__e)return n.__e;return"function"==typeof t.type?C(t):null}function x(t){var e,n;if(null!=(t=t.__)&&null!=t.__c){for(t.__e=t.__c.base=null,e=0;e<t.__k.length;e++)if(null!=(n=t.__k[e])&&null!=n.__e){t.__e=t.__c.base=n.__e;break}return x(t)}}function N(t){(!t.__d&&(t.__d=!0)&&f.push(t)&&!E.__r++||d!==c.debounceRendering)&&((d=c.debounceRendering)||setTimeout)(E)}function E(){for(var t;E.__r=f.length;)t=f.sort(function(t,e){return t.__v.__b-e.__v.__b}),f=[],t.some(function(t){var e,n,r,i,o,s;t.__d&&(o=(i=(e=t).__v).__e,(s=e.__P)&&(n=[],(r=y({},i)).__v=i.__v+1,U(s,i,r,e.__n,void 0!==s.ownerSVGElement,null!=i.__h?[o]:null,n,null==o?C(i):o,i.__h),H(n,i),i.__e!=o&&x(i)))})}function F(t,e,n,r,i,o,s,a,u,l){var c,p,h,f,d,_,v,y=r&&r.__k||g,b=y.length;for(n.__k=[],c=0;c<e.length;c++)if(null!=(f=n.__k[c]=null==(f=e[c])||"boolean"==typeof f?null:"string"==typeof f||"number"==typeof f||"bigint"==typeof f?P(null,f,null,null,f):Array.isArray(f)?P(S,{children:f},null,null,null):f.__b>0?P(f.type,f.props,f.key,null,f.__v):f)){if(f.__=n,f.__b=n.__b+1,null===(h=y[c])||h&&f.key==h.key&&f.type===h.type)y[c]=void 0;else for(p=0;p<b;p++){if((h=y[p])&&f.key==h.key&&f.type===h.type){y[p]=void 0;break}h=null}U(t,f,h=h||m,i,o,s,a,u,l),d=f.__e,(p=f.ref)&&h.ref!=p&&(v||(v=[]),h.ref&&v.push(h.ref,null,f),v.push(p,f.__c||d,f)),null!=d?(null==_&&(_=d),"function"==typeof f.type&&f.__k===h.__k?f.__d=u=T(f,u,t):u=D(t,f,h,y,d,u),"function"==typeof n.type&&(n.__d=u)):u&&h.__e==u&&u.parentNode!=t&&(u=C(h))}for(n.__e=_,c=b;c--;)null!=y[c]&&("function"==typeof n.type&&null!=y[c].__e&&y[c].__e==n.__d&&(n.__d=C(r,c+1)),j(y[c],y[c]));if(v)for(c=0;c<v.length;c++)O(v[c],v[++c],v[++c])}function T(t,e,n){for(var r,i=t.__k,o=0;i&&o<i.length;o++)(r=i[o])&&(r.__=t,e="function"==typeof r.type?T(r,e,n):D(n,r,r,i,r.__e,e));return e}function D(t,e,n,r,i,o){var s,a,u;if(void 0!==e.__d)s=e.__d,e.__d=void 0;else if(null==n||i!=o||null==i.parentNode)t:if(null==o||o.parentNode!==t)t.appendChild(i),s=null;else{for(a=o,u=0;(a=a.nextSibling)&&u<r.length;u+=2)if(a==i)break t;t.insertBefore(i,o),s=o}return void 0!==s?s:i.nextSibling}function R(t,e,n){"-"===e[0]?t.setProperty(e,n):t[e]=null==n?"":"number"!=typeof n||v.test(e)?n:n+"px"}function A(t,e,n,r,i){var o;t:if("style"===e)if("string"==typeof n)t.style.cssText=n;else{if("string"==typeof r&&(t.style.cssText=r=""),r)for(e in r)n&&e in n||R(t.style,e,"");if(n)for(e in n)r&&n[e]===r[e]||R(t.style,e,n[e])}else if("o"===e[0]&&"n"===e[1])o=e!==(e=e.replace(/Capture$/,"")),e=e.toLowerCase()in t?e.toLowerCase().slice(2):e.slice(2),t.l||(t.l={}),t.l[e+o]=n,n?r||t.addEventListener(e,o?I:L,o):t.removeEventListener(e,o?I:L,o);else if("dangerouslySetInnerHTML"!==e){if(i)e=e.replace(/xlink(H|:h)/,"h").replace(/sName$/,"s");else if("href"!==e&&"list"!==e&&"form"!==e&&"tabIndex"!==e&&"download"!==e&&e in t)try{t[e]=null==n?"":n;break t}catch(t){}"function"==typeof n||(null!=n&&(!1!==n||"a"===e[0]&&"r"===e[1])?t.setAttribute(e,n):t.removeAttribute(e))}}function L(t){this.l[t.type+!1](c.event?c.event(t):t)}function I(t){this.l[t.type+!0](c.event?c.event(t):t)}function U(t,e,n,r,i,o,s,a,u){var l,p,h,f,d,_,m,g,v,b,w,P,C,x=e.type;if(void 0!==e.constructor)return null;null!=n.__h&&(u=n.__h,a=e.__e=n.__e,e.__h=null,o=[a]),(l=c.__b)&&l(e);try{t:if("function"==typeof x){if(g=e.props,v=(l=x.contextType)&&r[l.__c],b=l?v?v.props.value:l.__:r,n.__c?m=(p=e.__c=n.__c).__=p.__E:("prototype"in x&&x.prototype.render?e.__c=p=new x(g,b):(e.__c=p=new k(g,b),p.constructor=x,p.render=W),v&&v.sub(p),p.props=g,p.state||(p.state={}),p.context=b,p.__n=r,h=p.__d=!0,p.__h=[]),null==p.__s&&(p.__s=p.state),null!=x.getDerivedStateFromProps&&(p.__s==p.state&&(p.__s=y({},p.__s)),y(p.__s,x.getDerivedStateFromProps(g,p.__s))),f=p.props,d=p.state,h)null==x.getDerivedStateFromProps&&null!=p.componentWillMount&&p.componentWillMount(),null!=p.componentDidMount&&p.__h.push(p.componentDidMount);else{if(null==x.getDerivedStateFromProps&&g!==f&&null!=p.componentWillReceiveProps&&p.componentWillReceiveProps(g,b),!p.__e&&null!=p.shouldComponentUpdate&&!1===p.shouldComponentUpdate(g,p.__s,b)||e.__v===n.__v){p.props=g,p.state=p.__s,e.__v!==n.__v&&(p.__d=!1),p.__v=e,e.__e=n.__e,e.__k=n.__k,e.__k.forEach(function(t){t&&(t.__=e)}),p.__h.length&&s.push(p);break t}null!=p.componentWillUpdate&&p.componentWillUpdate(g,p.__s,b),null!=p.componentDidUpdate&&p.__h.push(function(){p.componentDidUpdate(f,d,_)})}if(p.context=b,p.props=g,p.__v=e,p.__P=t,w=c.__r,P=0,"prototype"in x&&x.prototype.render)p.state=p.__s,p.__d=!1,w&&w(e),l=p.render(p.props,p.state,p.context);else do{p.__d=!1,w&&w(e),l=p.render(p.props,p.state,p.context),p.state=p.__s}while(p.__d&&++P<25);p.state=p.__s,null!=p.getChildContext&&(r=y(y({},r),p.getChildContext())),h||null==p.getSnapshotBeforeUpdate||(_=p.getSnapshotBeforeUpdate(f,d)),C=null!=l&&l.type===S&&null==l.key?l.props.children:l,F(t,Array.isArray(C)?C:[C],e,n,r,i,o,s,a,u),p.base=e.__e,e.__h=null,p.__h.length&&s.push(p),m&&(p.__E=p.__=null),p.__e=!1}else null==o&&e.__v===n.__v?(e.__k=n.__k,e.__e=n.__e):e.__e=M(n.__e,e,n,r,i,o,s,u);(l=c.diffed)&&l(e)}catch(t){e.__v=null,(u||null!=o)&&(e.__e=a,e.__h=!!u,o[o.indexOf(a)]=null),c.__e(t,e,n)}}function H(t,e){c.__c&&c.__c(e,t),t.some(function(e){try{t=e.__h,e.__h=[],t.some(function(t){t.call(e)})}catch(t){c.__e(t,e.__v)}})}function M(t,e,n,r,i,o,s,a){var u,c,p,h=n.props,f=e.props,d=e.type,_=0;if("svg"===d&&(i=!0),null!=o)for(;_<o.length;_++)if((u=o[_])&&"setAttribute"in u==!!d&&(d?u.localName===d:3===u.nodeType)){t=u,o[_]=null;break}if(null==t){if(null===d)return document.createTextNode(f);t=i?document.createElementNS("http://www.w3.org/2000/svg",d):document.createElement(d,f.is&&f),o=null,a=!1}if(null===d)h===f||a&&t.data===f||(t.data=f);else{if(o=o&&l.call(t.childNodes),c=(h=n.props||m).dangerouslySetInnerHTML,p=f.dangerouslySetInnerHTML,!a){if(null!=o)for(h={},_=0;_<t.attributes.length;_++)h[t.attributes[_].name]=t.attributes[_].value;(p||c)&&(p&&(c&&p.__html==c.__html||p.__html===t.innerHTML)||(t.innerHTML=p&&p.__html||""))}if(function(t,e,n,r,i){var o;for(o in n)"children"===o||"key"===o||o in e||A(t,o,null,n[o],r);for(o in e)i&&"function"!=typeof e[o]||"children"===o||"key"===o||"value"===o||"checked"===o||n[o]===e[o]||A(t,o,e[o],n[o],r)}(t,f,h,i,a),p)e.__k=[];else if(_=e.props.children,F(t,Array.isArray(_)?_:[_],e,n,r,i&&"foreignObject"!==d,o,s,o?o[0]:n.__k&&C(n,0),a),null!=o)for(_=o.length;_--;)null!=o[_]&&b(o[_]);a||("value"in f&&void 0!==(_=f.value)&&(_!==t.value||"progress"===d&&!_||"option"===d&&_!==h.value)&&A(t,"value",_,h.value,!1),"checked"in f&&void 0!==(_=f.checked)&&_!==t.checked&&A(t,"checked",_,h.checked,!1))}return t}function O(t,e,n){try{"function"==typeof t?t(e):t.current=e}catch(t){c.__e(t,n)}}function j(t,e,n){var r,i;if(c.unmount&&c.unmount(t),(r=t.ref)&&(r.current&&r.current!==t.__e||O(r,null,e)),null!=(r=t.__c)){if(r.componentWillUnmount)try{r.componentWillUnmount()}catch(t){c.__e(t,e)}r.base=r.__P=null}if(r=t.__k)for(i=0;i<r.length;i++)r[i]&&j(r[i],e,"function"!=typeof t.type);n||null==t.__e||b(t.__e),t.__e=t.__d=void 0}function W(t,e,n){return this.constructor(t,n)}function B(t,e,n){var r,i,o;c.__&&c.__(t,e),i=(r="function"==typeof n)?null:n&&n.__k||e.__k,o=[],U(e,t=(!r&&n||e).__k=w(S,null,[t]),i||m,m,void 0!==e.ownerSVGElement,!r&&n?[n]:i?null:e.firstChild?l.call(e.childNodes):null,o,!r&&n?n:i?i.__e:e.firstChild,r),H(o,t)}function z(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(t){var e=16*Math.random()|0;return("x"==t?e:3&e|8).toString(16)})}l=g.slice,c={__e:function(t,e,n,r){for(var i,o,s;e=e.__;)if((i=e.__c)&&!i.__)try{if((o=i.constructor)&&null!=o.getDerivedStateFromError&&(i.setState(o.getDerivedStateFromError(t)),s=i.__d),null!=i.componentDidCatch&&(i.componentDidCatch(t,r||{}),s=i.__d),s)return i.__E=i}catch(e){t=e}throw t}},p=0,h=function(t){return null!=t&&void 0===t.constructor},k.prototype.setState=function(t,e){var n;n=null!=this.__s&&this.__s!==this.state?this.__s:this.__s=y({},this.state),"function"==typeof t&&(t=t(y({},n),this.props)),t&&y(n,t),null!=t&&this.__v&&(e&&this.__h.push(e),N(this))},k.prototype.forceUpdate=function(t){this.__v&&(this.__e=!0,t&&this.__h.push(t),N(this))},k.prototype.render=S,f=[],E.__r=0,_=0;var q=/*#__PURE__*/function(){function t(t){this._id=void 0,this._id=t||z()}return n(t,[{key:"id",get:function(){return this._id}}]),t}(),V={search:{placeholder:"Type a keyword..."},sort:{sortAsc:"Sort column ascending",sortDesc:"Sort column descending"},pagination:{previous:"Previous",next:"Next",navigate:function(t,e){return"Page "+t+" of "+e},page:function(t){return"Page "+t},showing:"Showing",of:"of",to:"to",results:"results"},loading:"Loading...",noRecordsFound:"No matching records found",error:"An error happened while fetching the data"},G=/*#__PURE__*/function(){function t(t){this._language=void 0,this._defaultLanguage=void 0,this._language=t,this._defaultLanguage=V}var e=t.prototype;return e.getString=function(t,e){if(!e||!t)return null;var n=t.split("."),r=n[0];if(e[r]){var i=e[r];return"string"==typeof i?function(){return i}:"function"==typeof i?i:this.getString(n.slice(1).join("."),i)}return null},e.translate=function(t){var e,n=this.getString(t,this._language);return(e=n||this.getString(t,this._defaultLanguage))?e.apply(void 0,[].slice.call(arguments,1)):t},t}(),X=/*#__PURE__*/function(t){function e(e,n){var r,i;return(r=t.call(this,e,n)||this).config=void 0,r._=void 0,r.config=function(t){if(!t)return null;var e=Object.keys(t);return e.length?t[e[0]].props.value:null}(n),r.config&&(r._=(i=r.config.translator,function(t){return i.translate.apply(i,[t].concat([].slice.call(arguments,1)))})),r}return i(e,t),e}(k),$=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype.render=function(){return w(this.props.parentElement,{dangerouslySetInnerHTML:{__html:this.props.content}})},e}(X);function K(t,e){return w($,{content:t,parentElement:e})}$.defaultProps={parentElement:"span"};var Y,Z=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this).data=void 0,n.update(e),n}i(e,t);var n=e.prototype;return n.cast=function(t){return t instanceof HTMLElement?K(t.outerHTML):t},n.update=function(t){return this.data=this.cast(t),this},e}(q),J=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this)._cells=void 0,n.cells=e||[],n}i(e,t);var r=e.prototype;return r.cell=function(t){return this._cells[t]},r.toArray=function(){return this.cells.map(function(t){return t.data})},e.fromCells=function(t){return new e(t.map(function(t){return new Z(t.data)}))},n(e,[{key:"cells",get:function(){return this._cells},set:function(t){this._cells=t}},{key:"length",get:function(){return this.cells.length}}]),e}(q),Q=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this)._rows=void 0,n._length=void 0,n.rows=e instanceof Array?e:e instanceof J?[e]:[],n}return i(e,t),e.prototype.toArray=function(){return this.rows.map(function(t){return t.toArray()})},e.fromRows=function(t){return new e(t.map(function(t){return J.fromCells(t.cells)}))},e.fromArray=function(t){return new e((t=function(t){return!t[0]||t[0]instanceof Array?t:[t]}(t)).map(function(t){return new J(t.map(function(t){return new Z(t)}))}))},n(e,[{key:"rows",get:function(){return this._rows},set:function(t){this._rows=t}},{key:"length",get:function(){return this._length||this.rows.length},set:function(t){this._length=t}}]),e}(q),tt=/*#__PURE__*/function(){function t(){this.callbacks=void 0}var e=t.prototype;return e.init=function(t){this.callbacks||(this.callbacks={}),t&&!this.callbacks[t]&&(this.callbacks[t]=[])},e.on=function(t,e){return this.init(t),this.callbacks[t].push(e),this},e.off=function(t,e){var n=t;return this.init(),this.callbacks[n]&&0!==this.callbacks[n].length?(this.callbacks[n]=this.callbacks[n].filter(function(t){return t!=e}),this):this},e.emit=function(t){var e=arguments,n=t;return this.init(n),this.callbacks[n].length>0&&(this.callbacks[n].forEach(function(t){return t.apply(void 0,[].slice.call(e,1))}),!0)},t}();!function(t){t[t.Initiator=0]="Initiator",t[t.ServerFilter=1]="ServerFilter",t[t.ServerSort=2]="ServerSort",t[t.ServerLimit=3]="ServerLimit",t[t.Extractor=4]="Extractor",t[t.Transformer=5]="Transformer",t[t.Filter=6]="Filter",t[t.Sort=7]="Sort",t[t.Limit=8]="Limit"}(Y||(Y={}));var et=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this).id=void 0,n._props=void 0,n._props={},n.id=z(),e&&n.setProps(e),n}i(e,t);var r=e.prototype;return r.process=function(){var t=[].slice.call(arguments);this.validateProps instanceof Function&&this.validateProps.apply(this,t),this.emit.apply(this,["beforeProcess"].concat(t));var e=this._process.apply(this,t);return this.emit.apply(this,["afterProcess"].concat(t)),e},r.setProps=function(t){return Object.assign(this._props,t),this.emit("propsUpdated",this),this},n(e,[{key:"props",get:function(){return this._props}}]),e}(tt),nt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype._process=function(t){return this.props.keyword?(e=String(this.props.keyword).trim(),n=this.props.columns,r=this.props.ignoreHiddenColumns,i=t,o=this.props.selector,e=e.replace(/[-[\]{}()*+?.,\\^$|#\s]/g,"\\$&"),new Q(i.rows.filter(function(t,i){return t.cells.some(function(t,s){if(!t)return!1;if(r&&n&&n[s]&&"object"==typeof n[s]&&n[s].hidden)return!1;var a="";if("function"==typeof o)a=o(t.data,i,s);else if("object"==typeof t.data){var u=t.data;u&&u.props&&u.props.content&&(a=u.props.content)}else a=String(t.data);return new RegExp(e,"gi").test(a)})}))):t;var e,n,r,i,o},n(e,[{key:"type",get:function(){return Y.Filter}}]),e}(et);function rt(){var t="gridjs";return""+t+[].slice.call(arguments).reduce(function(t,e){return t+"-"+e},"")}function it(){return[].slice.call(arguments).filter(function(t){return t}).reduce(function(t,e){return(t||"")+" "+e},"").trim()||null}var ot,st=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this)._state=void 0,n.dispatcher=void 0,n.dispatcher=e,n._state=n.getInitialState(),e.register(n._handle.bind(s(n))),n}i(e,t);var r=e.prototype;return r._handle=function(t){this.handle(t.type,t.payload)},r.setState=function(t){var e=this._state;this._state=t,this.emit("updated",t,e)},n(e,[{key:"state",get:function(){return this._state}}]),e}(tt),at=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var n=e.prototype;return n.getInitialState=function(){return{keyword:null}},n.handle=function(t,e){"SEARCH_KEYWORD"===t&&this.search(e.keyword)},n.search=function(t){this.setState({keyword:t})},e}(st),ut=/*#__PURE__*/function(){function t(t){this.dispatcher=void 0,this.dispatcher=t}return t.prototype.dispatch=function(t,e){this.dispatcher.dispatch({type:t,payload:e})},t}(),lt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype.search=function(t){this.dispatch("SEARCH_KEYWORD",{keyword:t})},e}(ut),ct=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype._process=function(t){if(!this.props.keyword)return t;var e={};return this.props.url&&(e.url=this.props.url(t.url,this.props.keyword)),this.props.body&&(e.body=this.props.body(t.body,this.props.keyword)),r({},t,e)},n(e,[{key:"type",get:function(){return Y.ServerFilter}}]),e}(et),pt=new(/*#__PURE__*/function(){function t(){}var e=t.prototype;return e.format=function(t,e){return"[Grid.js] ["+e.toUpperCase()+"]: "+t},e.error=function(t,e){void 0===e&&(e=!1);var n=this.format(t,"error");if(e)throw Error(n);console.error(n)},e.warn=function(t){console.warn(this.format(t,"warn"))},e.info=function(t){console.info(this.format(t,"info"))},t}()),ht=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e}(X);t.PluginPosition=void 0,(ot=t.PluginPosition||(t.PluginPosition={}))[ot.Header=0]="Header",ot[ot.Footer=1]="Footer",ot[ot.Cell=2]="Cell";var ft=/*#__PURE__*/function(){function t(){this.plugins=void 0,this.plugins=[]}var e=t.prototype;return e.get=function(t){var e=this.plugins.filter(function(e){return e.id===t});return e.length>0?e[0]:null},e.add=function(t){return t.id?null!==this.get(t.id)?(pt.error("Duplicate plugin ID: "+t.id),this):(this.plugins.push(t),this):(pt.error("Plugin ID cannot be empty"),this)},e.remove=function(t){return this.plugins.splice(this.plugins.indexOf(this.get(t)),1),this},e.list=function(t){var e;return e=null!=t||null!=t?this.plugins.filter(function(e){return e.position===t}):this.plugins,e.sort(function(t,e){return t.order-e.order})},t}(),dt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype.render=function(){var t=this;if(this.props.pluginId){var e=this.config.plugin.get(this.props.pluginId);return e?w(S,{},w(e.component,r({plugin:e},e.props,this.props.props))):null}return void 0!==this.props.position?w(S,{},this.config.plugin.list(this.props.position).map(function(e){return w(e.component,r({plugin:e},e.props,t.props.props))})):null},e}(X),_t=/*#__PURE__*/function(t){function e(e,n){var r;(r=t.call(this,e,n)||this).searchProcessor=void 0,r.actions=void 0,r.store=void 0,r.storeUpdatedFn=void 0,r.actions=new lt(r.config.dispatcher),r.store=new at(r.config.dispatcher);var i,o=e.keyword;return e.enabled&&(o&&r.actions.search(o),r.storeUpdatedFn=r.storeUpdated.bind(s(r)),r.store.on("updated",r.storeUpdatedFn),i=e.server?new ct({keyword:e.keyword,url:e.server.url,body:e.server.body}):new nt({keyword:e.keyword,columns:r.config.header&&r.config.header.columns,ignoreHiddenColumns:e.ignoreHiddenColumns||void 0===e.ignoreHiddenColumns,selector:e.selector}),r.searchProcessor=i,r.config.pipeline.register(i)),r}i(e,t);var n=e.prototype;return n.componentWillUnmount=function(){this.config.pipeline.unregister(this.searchProcessor),this.store.off("updated",this.storeUpdatedFn)},n.storeUpdated=function(t){this.searchProcessor.setProps({keyword:t.keyword})},n.onChange=function(t){this.actions.search(t.target.value)},n.render=function(){if(!this.props.enabled)return null;var t,e,n,r=this.onChange.bind(this);return this.searchProcessor instanceof ct&&(t=r,e=this.props.debounceTimeout,r=function(){var r=arguments;return new Promise(function(i){n&&clearTimeout(n),n=setTimeout(function(){return i(t.apply(void 0,[].slice.call(r)))},e)})}),w("div",{className:rt(it("search",this.config.className.search))},w("input",{type:"search",placeholder:this._("search.placeholder"),"aria-label":this._("search.placeholder"),onInput:r,className:it(rt("input"),rt("search","input")),value:this.store.state.keyword}))},e}(ht);_t.defaultProps={debounceTimeout:250};var mt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var r=e.prototype;return r.validateProps=function(){if(isNaN(Number(this.props.limit))||isNaN(Number(this.props.page)))throw Error("Invalid parameters passed")},r._process=function(t){var e=this.props.page;return new Q(t.rows.slice(e*this.props.limit,(e+1)*this.props.limit))},n(e,[{key:"type",get:function(){return Y.Limit}}]),e}(et),gt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype._process=function(t){var e={};return this.props.url&&(e.url=this.props.url(t.url,this.props.page,this.props.limit)),this.props.body&&(e.body=this.props.body(t.body,this.props.page,this.props.limit)),r({},t,e)},n(e,[{key:"type",get:function(){return Y.ServerLimit}}]),e}(et),vt=/*#__PURE__*/function(t){function e(e,n){var r;return(r=t.call(this,e,n)||this).processor=void 0,r.onUpdateFn=void 0,r.setTotalFromTabularFn=void 0,r.state={limit:e.limit,page:e.page||0,total:0},r}i(e,t);var r=e.prototype;return r.componentWillMount=function(){var t,e=this;this.props.enabled&&(this.setTotalFromTabularFn=this.setTotalFromTabular.bind(this),this.props.server?(t=new gt({limit:this.state.limit,page:this.state.page,url:this.props.server.url,body:this.props.server.body}),this.config.pipeline.on("afterProcess",this.setTotalFromTabularFn)):(t=new mt({limit:this.state.limit,page:this.state.page})).on("beforeProcess",this.setTotalFromTabularFn),this.processor=t,this.config.pipeline.register(t),this.config.pipeline.on("error",function(){e.setState({total:0,page:0})}))},r.setTotalFromTabular=function(t){this.setTotal(t.length)},r.onUpdate=function(t){this.props.resetPageOnUpdate&&t!==this.processor&&this.setPage(0)},r.componentDidMount=function(){this.onUpdateFn=this.onUpdate.bind(this),this.config.pipeline.on("updated",this.onUpdateFn)},r.componentWillUnmount=function(){this.config.pipeline.unregister(this.processor),this.config.pipeline.off("updated",this.onUpdateFn)},r.setPage=function(t){if(t>=this.pages||t<0||t===this.state.page)return null;this.setState({page:t}),this.processor.setProps({page:t})},r.setTotal=function(t){this.setState({total:t})},r.renderPages=function(){var t=this;if(this.props.buttonsCount<=0)return null;var e=Math.min(this.pages,this.props.buttonsCount),n=Math.min(this.state.page,Math.floor(e/2));return this.state.page+Math.floor(e/2)>=this.pages&&(n=e-(this.pages-this.state.page)),w(S,null,this.pages>e&&this.state.page-n>0&&w(S,null,w("button",{tabIndex:0,role:"button",onClick:this.setPage.bind(this,0),title:this._("pagination.firstPage"),"aria-label":this._("pagination.firstPage"),className:this.config.className.paginationButton},this._("1")),w("button",{tabIndex:-1,className:it(rt("spread"),this.config.className.paginationButton)},"...")),Array.from(Array(e).keys()).map(function(e){return t.state.page+(e-n)}).map(function(e){return w("button",{tabIndex:0,role:"button",onClick:t.setPage.bind(t,e),className:it(t.state.page===e?it(rt("currentPage"),t.config.className.paginationButtonCurrent):null,t.config.className.paginationButton),title:t._("pagination.page",e+1),"aria-label":t._("pagination.page",e+1)},t._(""+(e+1)))}),this.pages>e&&this.pages>this.state.page+n+1&&w(S,null,w("button",{tabIndex:-1,className:it(rt("spread"),this.config.className.paginationButton)},"..."),w("button",{tabIndex:0,role:"button",onClick:this.setPage.bind(this,this.pages-1),title:this._("pagination.page",this.pages),"aria-label":this._("pagination.page",this.pages),className:this.config.className.paginationButton},this._(""+this.pages))))},r.renderSummary=function(){return w(S,null,this.props.summary&&this.state.total>0&&w("div",{role:"status","aria-live":"polite",className:it(rt("summary"),this.config.className.paginationSummary),title:this._("pagination.navigate",this.state.page+1,this.pages)},this._("pagination.showing")," ",w("b",null,this._(""+(this.state.page*this.state.limit+1)))," ",this._("pagination.to")," ",w("b",null,this._(""+Math.min((this.state.page+1)*this.state.limit,this.state.total)))," ",this._("pagination.of")," ",w("b",null,this._(""+this.state.total))," ",this._("pagination.results")))},r.render=function(){return this.props.enabled?w("div",{className:it(rt("pagination"),this.config.className.pagination)},this.renderSummary(),w("div",{className:rt("pages")},this.props.prevButton&&w("button",{tabIndex:0,role:"button",disabled:0===this.state.page,onClick:this.setPage.bind(this,this.state.page-1),title:this._("pagination.previous"),"aria-label":this._("pagination.previous"),className:it(this.config.className.paginationButton,this.config.className.paginationButtonPrev)},this._("pagination.previous")),this.renderPages(),this.props.nextButton&&w("button",{tabIndex:0,role:"button",disabled:this.pages===this.state.page+1||0===this.pages,onClick:this.setPage.bind(this,this.state.page+1),title:this._("pagination.next"),"aria-label":this._("pagination.next"),className:it(this.config.className.paginationButton,this.config.className.paginationButtonNext)},this._("pagination.next")))):null},n(e,[{key:"pages",get:function(){return Math.ceil(this.state.total/this.state.limit)}}]),e}(ht);function yt(t,e){return"string"==typeof t?t.indexOf("%")>-1?e/100*parseInt(t,10):parseInt(t,10):t}function bt(t){return t?Math.floor(t)+"px":""}vt.defaultProps={summary:!0,nextButton:!0,prevButton:!0,buttonsCount:3,limit:10,resetPageOnUpdate:!0};var wt=/*#__PURE__*/function(t){function e(e,n){var r;return(r=t.call(this,e,n)||this).tableElement=void 0,r.tableClassName=void 0,r.tableStyle=void 0,r.tableElement=r.props.tableRef.current.base.cloneNode(!0),r.tableElement.style.position="absolute",r.tableElement.style.width="100%",r.tableElement.style.zIndex="-2147483640",r.tableElement.style.visibility="hidden",r.tableClassName=r.tableElement.className,r.tableStyle=r.tableElement.style.cssText,r}i(e,t);var n=e.prototype;return n.widths=function(){this.tableElement.className=this.tableClassName+" "+rt("shadowTable"),this.tableElement.style.tableLayout="auto",this.tableElement.style.width="auto",this.tableElement.style.padding="0",this.tableElement.style.margin="0",this.tableElement.style.border="none",this.tableElement.style.outline="none";var t=Array.from(this.base.parentNode.querySelectorAll("thead th")).reduce(function(t,e){var n;return e.style.width=e.clientWidth+"px",r(((n={})[e.getAttribute("data-column-id")]={minWidth:e.clientWidth},n),t)},{});return this.tableElement.className=this.tableClassName,this.tableElement.style.cssText=this.tableStyle,this.tableElement.style.tableLayout="auto",Array.from(this.base.parentNode.querySelectorAll("thead th")).reduce(function(t,e){return t[e.getAttribute("data-column-id")].width=e.clientWidth,t},t)},n.render=function(){var t=this;return this.props.tableRef.current?w("div",{ref:function(e){e&&e.appendChild(t.tableElement)}}):null},e}(X);function Pt(t){if(!t)return"";var e=t.split(" ");return 1===e.length&&/([a-z][A-Z])+/g.test(t)?t:e.map(function(t,e){return 0==e?t.toLowerCase():t.charAt(0).toUpperCase()+t.slice(1).toLowerCase()}).join("")}var St=/*#__PURE__*/function(e){function o(){var t;return(t=e.call(this)||this)._columns=void 0,t._columns=[],t}i(o,e);var s=o.prototype;return s.adjustWidth=function(t){var e=t.container,n=t.tableRef,r=t.tempRef,i=t.tempRef||!0;if(!e)return this;var s=e.clientWidth,a={current:null},l={};if(n.current&&i){var c=w(wt,{tableRef:n});c.ref=a,B(c,r.current),l=a.current.widths()}for(var p,h=u(o.tabularFormat(this.columns).reduce(function(t,e){return t.concat(e)},[]));!(p=h()).done;){var f=p.value;f.columns&&f.columns.length>0||(!f.width&&i?f.id in l&&(f.width=bt(l[f.id].width),f.minWidth=bt(l[f.id].minWidth)):f.width=bt(yt(f.width,s)))}return n.current&&i&&B(null,r.current),this},s.setSort=function(t,e){for(var n,i=u(e||this.columns||[]);!(n=i()).done;){var o=n.value;o.columns&&o.columns.length>0&&(o.sort={enabled:!1}),void 0===o.sort&&t.sort&&(o.sort={enabled:!0}),o.sort?"object"==typeof o.sort&&(o.sort=r({enabled:!0},o.sort)):o.sort={enabled:!1},o.columns&&this.setSort(t,o.columns)}},s.setFixedHeader=function(t,e){for(var n,r=u(e||this.columns||[]);!(n=r()).done;){var i=n.value;void 0===i.fixedHeader&&(i.fixedHeader=t.fixedHeader),i.columns&&this.setFixedHeader(t,i.columns)}},s.setResizable=function(t,e){for(var n,r=u(e||this.columns||[]);!(n=r()).done;){var i=n.value;void 0===i.resizable&&(i.resizable=t.resizable),i.columns&&this.setResizable(t,i.columns)}},s.setID=function(t){for(var e,n=u(t||this.columns||[]);!(e=n()).done;){var r=e.value;r.id||"string"!=typeof r.name||(r.id=Pt(r.name)),r.id||pt.error('Could not find a valid ID for one of the columns. Make sure a valid "id" is set for all columns.'),r.columns&&this.setID(r.columns)}},s.populatePlugins=function(e,n){for(var i,o=u(n);!(i=o()).done;){var s=i.value;void 0!==s.plugin&&e.plugin.add(r({id:s.id,props:{}},s.plugin,{position:t.PluginPosition.Cell}))}},o.fromColumns=function(t){for(var e,n=new o,r=u(t);!(e=r()).done;){var i=e.value;if("string"==typeof i||h(i))n.columns.push({name:i});else if("object"==typeof i){var s=i;s.columns&&(s.columns=o.fromColumns(s.columns).columns),"object"==typeof s.plugin&&void 0===s.data&&(s.data=null),n.columns.push(i)}}return n},o.fromUserConfig=function(t){var e=new o;return t.from?e.columns=o.fromHTMLTable(t.from).columns:t.columns?e.columns=o.fromColumns(t.columns).columns:!t.data||"object"!=typeof t.data[0]||t.data[0]instanceof Array||(e.columns=Object.keys(t.data[0]).map(function(t){return{name:t}})),e.columns.length?(e.setID(),e.setSort(t),e.setFixedHeader(t),e.setResizable(t),e.populatePlugins(t,e.columns),e):null},o.fromHTMLTable=function(t){for(var e,n=new o,r=u(t.querySelector("thead").querySelectorAll("th"));!(e=r()).done;){var i=e.value;n.columns.push({name:i.innerHTML,width:i.width})}return n},o.tabularFormat=function(t){var e=[],n=t||[],r=[];if(n&&n.length){e.push(n);for(var i,o=u(n);!(i=o()).done;){var s=i.value;s.columns&&s.columns.length&&(r=r.concat(s.columns))}r.length&&(e=e.concat(this.tabularFormat(r)))}return e},o.leafColumns=function(t){var e=[],n=t||[];if(n&&n.length)for(var r,i=u(n);!(r=i()).done;){var o=r.value;o.columns&&0!==o.columns.length||e.push(o),o.columns&&(e=e.concat(this.leafColumns(o.columns)))}return e},o.maximumDepth=function(t){return this.tabularFormat([t]).length-1},n(o,[{key:"columns",get:function(){return this._columns},set:function(t){this._columns=t}},{key:"visibleColumns",get:function(){return this._columns.filter(function(t){return!t.hidden})}}]),o}(q),kt=/*#__PURE__*/function(){function t(){this._callbacks=void 0,this._isDispatching=void 0,this._isHandled=void 0,this._isPending=void 0,this._lastID=void 0,this._pendingPayload=void 0,this._callbacks={},this._isDispatching=!1,this._isHandled={},this._isPending={},this._lastID=1}var e=t.prototype;return e.register=function(t){var e="ID_"+this._lastID++;return this._callbacks[e]=t,e},e.unregister=function(t){if(!this._callbacks[t])throw Error("Dispatcher.unregister(...): "+t+" does not map to a registered callback.");delete this._callbacks[t]},e.waitFor=function(t){if(!this._isDispatching)throw Error("Dispatcher.waitFor(...): Must be invoked while dispatching.");for(var e=0;e<t.length;e++){var n=t[e];if(this._isPending[n]){if(!this._isHandled[n])throw Error("Dispatcher.waitFor(...): Circular dependency detected while ' +\n            'waiting for "+n+".")}else{if(!this._callbacks[n])throw Error("Dispatcher.waitFor(...): "+n+" does not map to a registered callback.");this._invokeCallback(n)}}},e.dispatch=function(t){if(this._isDispatching)throw Error("Dispatch.dispatch(...): Cannot dispatch in the middle of a dispatch.");this._startDispatching(t);try{for(var e in this._callbacks)this._isPending[e]||this._invokeCallback(e)}finally{this._stopDispatching()}},e.isDispatching=function(){return this._isDispatching},e._invokeCallback=function(t){this._isPending[t]=!0,this._callbacks[t](this._pendingPayload),this._isHandled[t]=!0},e._startDispatching=function(t){for(var e in this._callbacks)this._isPending[e]=!1,this._isHandled[e]=!1;this._pendingPayload=t,this._isDispatching=!0},e._stopDispatching=function(){delete this._pendingPayload,this._isDispatching=!1},t}(),Ct=function(){},xt=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this).data=void 0,n.set(e),n}i(e,t);var n=e.prototype;return n.get=function(){try{return Promise.resolve(this.data()).then(function(t){return{data:t,total:t.length}})}catch(t){return Promise.reject(t)}},n.set=function(t){return t instanceof Array?this.data=function(){return t}:t instanceof Function&&(this.data=t),this},e}(Ct),Nt=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this).options=void 0,n.options=e,n}i(e,t);var n=e.prototype;return n.handler=function(t){return"function"==typeof this.options.handle?this.options.handle(t):t.ok?t.json():(pt.error("Could not fetch data: "+t.status+" - "+t.statusText,!0),null)},n.get=function(t){var e=r({},this.options,t);return"function"==typeof e.data?e.data(e):fetch(e.url,e).then(this.handler.bind(this)).then(function(t){return{data:e.then(t),total:"function"==typeof e.total?e.total(t):void 0}})},e}(Ct),Et=/*#__PURE__*/function(){function t(){}return t.createFromUserConfig=function(t){var e=null;return t.data&&(e=new xt(t.data)),t.from&&(e=new xt(this.tableElementToArray(t.from)),t.from.style.display="none"),t.server&&(e=new Nt(t.server)),e||pt.error("Could not determine the storage type",!0),e},t.tableElementToArray=function(t){for(var e,n,r=[],i=u(t.querySelector("tbody").querySelectorAll("tr"));!(e=i()).done;){for(var o,s=[],a=u(e.value.querySelectorAll("td"));!(o=a()).done;){var l=o.value;1===l.childNodes.length&&l.childNodes[0].nodeType===Node.TEXT_NODE?s.push((n=l.innerHTML,(new DOMParser).parseFromString(n,"text/html").documentElement.textContent)):s.push(K(l.innerHTML))}r.push(s)}return r},t}(),Ft="undefined"!=typeof Symbol?Symbol.iterator||(Symbol.iterator=Symbol("Symbol.iterator")):"@@iterator";function Tt(t,e,n){if(!t.s){if(n instanceof Dt){if(!n.s)return void(n.o=Tt.bind(null,t,e));1&e&&(e=n.s),n=n.v}if(n&&n.then)return void n.then(Tt.bind(null,t,e),Tt.bind(null,t,2));t.s=e,t.v=n;var r=t.o;r&&r(t)}}var Dt=/*#__PURE__*/function(){function t(){}return t.prototype.then=function(e,n){var r=new t,i=this.s;if(i){var o=1&i?e:n;if(o){try{Tt(r,1,o(this.v))}catch(t){Tt(r,2,t)}return r}return this}return this.o=function(t){try{var i=t.v;1&t.s?Tt(r,1,e?e(i):i):n?Tt(r,1,n(i)):Tt(r,2,i)}catch(t){Tt(r,2,t)}},r},t}();function Rt(t){return t instanceof Dt&&1&t.s}var At,Lt=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this)._steps=new Map,n.cache=new Map,n.lastProcessorIndexUpdated=-1,e&&e.forEach(function(t){return n.register(t)}),n}i(e,t);var r=e.prototype;return r.clearCache=function(){this.cache=new Map,this.lastProcessorIndexUpdated=-1},r.register=function(t,e){if(void 0===e&&(e=null),null===t.type)throw Error("Processor type is not defined");t.on("propsUpdated",this.processorPropsUpdated.bind(this)),this.addProcessorByPriority(t,e),this.afterRegistered(t)},r.unregister=function(t){if(t){var e=this._steps.get(t.type);e&&e.length&&(this._steps.set(t.type,e.filter(function(e){return e!=t})),this.emit("updated",t))}},r.addProcessorByPriority=function(t,e){var n=this._steps.get(t.type);if(!n){var r=[];this._steps.set(t.type,r),n=r}if(null===e||e<0)n.push(t);else if(n[e]){var i=n.slice(0,e-1),o=n.slice(e+1);this._steps.set(t.type,i.concat(t).concat(o))}else n[e]=t},r.getStepsByType=function(t){return this.steps.filter(function(e){return e.type===t})},r.getSortedProcessorTypes=function(){return Object.keys(Y).filter(function(t){return!isNaN(Number(t))}).map(function(t){return Number(t)})},r.process=function(t){try{var e=this,n=function(t){return e.lastProcessorIndexUpdated=i.length,e.emit("afterProcess",o),o},r=e.lastProcessorIndexUpdated,i=e.steps,o=t,s=function(t,n){try{var s=function(t,e,n){if("function"==typeof t[Ft]){var r,i,o,s=t[Ft]();if(function t(n){try{for(;!(r=s.next()).done;)if((n=e(r.value))&&n.then){if(!Rt(n))return void n.then(t,o||(o=Tt.bind(null,i=new Dt,2)));n=n.v}i?Tt(i,1,n):i=n}catch(t){Tt(i||(i=new Dt),2,t)}}(),s.return){var a=function(t){try{r.done||s.return()}catch(t){}return t};if(i&&i.then)return i.then(a,function(t){throw a(t)});a()}return i}if(!("length"in t))throw new TypeError("Object is not iterable");for(var u=[],l=0;l<t.length;l++)u.push(t[l]);return function(t,e,n){var r,i,o=-1;return function n(s){try{for(;++o<t.length;)if((s=e(o))&&s.then){if(!Rt(s))return void s.then(n,i||(i=Tt.bind(null,r=new Dt,2)));s=s.v}r?Tt(r,1,s):r=s}catch(t){Tt(r||(r=new Dt),2,t)}}(),r}(u,function(t){return e(u[t])})}(i,function(t){var n=e.findProcessorIndexByID(t.id),i=function(){if(n>=r)return Promise.resolve(t.process(o)).then(function(n){e.cache.set(t.id,o=n)});o=e.cache.get(t.id)}();if(i&&i.then)return i.then(function(){})})}catch(t){return n(t)}return s&&s.then?s.then(void 0,n):s}(0,function(t){throw pt.error(t),e.emit("error",o),t});return Promise.resolve(s&&s.then?s.then(n):n())}catch(t){return Promise.reject(t)}},r.findProcessorIndexByID=function(t){return this.steps.findIndex(function(e){return e.id==t})},r.setLastProcessorIndex=function(t){var e=this.findProcessorIndexByID(t.id);this.lastProcessorIndexUpdated>e&&(this.lastProcessorIndexUpdated=e)},r.processorPropsUpdated=function(t){this.setLastProcessorIndex(t),this.emit("propsUpdated"),this.emit("updated",t)},r.afterRegistered=function(t){this.setLastProcessorIndex(t),this.emit("afterRegister"),this.emit("updated",t)},n(e,[{key:"steps",get:function(){for(var t,e=[],n=u(this.getSortedProcessorTypes());!(t=n()).done;){var r=this._steps.get(t.value);r&&r.length&&(e=e.concat(r))}return e.filter(function(t){return t})}}]),e}(tt),It=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype._process=function(t){try{return Promise.resolve(this.props.storage.get(t))}catch(t){return Promise.reject(t)}},n(e,[{key:"type",get:function(){return Y.Extractor}}]),e}(et),Ut=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype._process=function(t){var e=Q.fromArray(t.data);return e.length=t.total,e},n(e,[{key:"type",get:function(){return Y.Transformer}}]),e}(et),Ht=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype._process=function(){return Object.entries(this.props.serverStorageOptions).filter(function(t){return"function"!=typeof t[1]}).reduce(function(t,e){var n;return r({},t,((n={})[e[0]]=e[1],n))},{})},n(e,[{key:"type",get:function(){return Y.Initiator}}]),e}(et),Mt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var r=e.prototype;return r.castData=function(t){if(!t||!t.length)return[];if(!this.props.header||!this.props.header.columns)return t;var e=St.leafColumns(this.props.header.columns);return t[0]instanceof Array?t.map(function(t){var n=0;return e.map(function(e,r){return void 0!==e.data?(n++,"function"==typeof e.data?e.data(t):e.data):t[r-n]})}):"object"!=typeof t[0]||t[0]instanceof Array?[]:t.map(function(t){return e.map(function(e,n){return void 0!==e.data?"function"==typeof e.data?e.data(t):e.data:e.id?t[e.id]:(pt.error("Could not find the correct cell for column at position "+n+".\n                          Make sure either 'id' or 'selector' is defined for all columns."),null)})})},r._process=function(t){return{data:this.castData(t.data),total:t.total}},n(e,[{key:"type",get:function(){return Y.Transformer}}]),e}(et),Ot=/*#__PURE__*/function(){function t(){}return t.createFromConfig=function(t){var e=new Lt;return t.storage instanceof Nt&&e.register(new Ht({serverStorageOptions:t.server})),e.register(new It({storage:t.storage})),e.register(new Mt({header:t.header})),e.register(new Ut),e},t}(),jt=/*#__PURE__*/function(){function e(t){this._userConfig=void 0,Object.assign(this,r({},e.defaultConfig(),t)),this._userConfig={}}var n=e.prototype;return n.assign=function(t){for(var e=0,n=Object.keys(t);e<n.length;e++){var r=n[e];"_userConfig"!==r&&(this[r]=t[r])}return this},n.update=function(t){return t?(this._userConfig=r({},this._userConfig,t),this.assign(e.fromUserConfig(this._userConfig)),this):this},e.defaultConfig=function(){return{plugin:new ft,dispatcher:new kt,tableRef:{current:null},tempRef:{current:null},width:"100%",height:"auto",autoWidth:!0,style:{},className:{}}},e.fromUserConfig=function(n){var i=new e(n);return i._userConfig=n,"boolean"==typeof n.sort&&n.sort&&i.assign({sort:{multiColumn:!0}}),i.assign({header:St.fromUserConfig(i)}),i.assign({storage:Et.createFromUserConfig(n)}),i.assign({pipeline:Ot.createFromConfig(i)}),i.assign({translator:new G(n.language)}),i.plugin.add({id:"search",position:t.PluginPosition.Header,component:_t,props:r({enabled:!0===n.search||n.search instanceof Object},n.search)}),i.plugin.add({id:"pagination",position:t.PluginPosition.Footer,component:vt,props:r({enabled:!0===n.pagination||n.pagination instanceof Object},n.pagination)}),n.plugins&&n.plugins.forEach(function(t){return i.plugin.add(t)}),i},e}();!function(t){t[t.Init=0]="Init",t[t.Loading=1]="Loading",t[t.Loaded=2]="Loaded",t[t.Rendered=3]="Rendered",t[t.Error=4]="Error"}(At||(At={}));var Wt,Bt,zt,qt,Vt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var n=e.prototype;return n.content=function(){return this.props.column&&"function"==typeof this.props.column.formatter?this.props.column.formatter(this.props.cell.data,this.props.row,this.props.column):this.props.column&&this.props.column.plugin?w(dt,{pluginId:this.props.column.id,props:{column:this.props.column,cell:this.props.cell,row:this.props.row}}):this.props.cell.data},n.handleClick=function(t){this.props.messageCell||this.config.eventEmitter.emit("cellClick",t,this.props.cell,this.props.column,this.props.row)},n.getCustomAttributes=function(t){return t?"function"==typeof t.attributes?t.attributes(this.props.cell.data,this.props.row,this.props.column):t.attributes:{}},n.render=function(){return w("td",r({role:this.props.role,colSpan:this.props.colSpan,"data-column-id":this.props.column&&this.props.column.id,className:it(rt("td"),this.props.className,this.config.className.td),style:r({},this.props.style,this.config.style.td),onClick:this.handleClick.bind(this)},this.getCustomAttributes(this.props.column)),this.content())},e}(X),Gt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var n=e.prototype;return n.getColumn=function(t){if(this.props.header){var e=St.leafColumns(this.props.header.columns);if(e)return e[t]}return null},n.handleClick=function(t){this.props.messageRow||this.config.eventEmitter.emit("rowClick",t,this.props.row)},n.getChildren=function(){var t=this;return this.props.children?this.props.children:w(S,null,this.props.row.cells.map(function(e,n){var r=t.getColumn(n);return r&&r.hidden?null:w(Vt,{key:e.id,cell:e,row:t.props.row,column:r})}))},n.render=function(){return w("tr",{className:it(rt("tr"),this.config.className.tr),onClick:this.handleClick.bind(this)},this.getChildren())},e}(X),Xt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype.render=function(){return w(Gt,{messageRow:!0},w(Vt,{role:"alert",colSpan:this.props.colSpan,messageCell:!0,cell:new Z(this.props.message),className:it(rt("message"),this.props.className?this.props.className:null)}))},e}(X),$t=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var n=e.prototype;return n.headerLength=function(){return this.props.header?this.props.header.visibleColumns.length:0},n.render=function(){var t=this;return w("tbody",{className:it(rt("tbody"),this.config.className.tbody)},this.props.data&&this.props.data.rows.map(function(e){return w(Gt,{key:e.id,row:e,header:t.props.header})}),this.props.status===At.Loading&&(!this.props.data||0===this.props.data.length)&&w(Xt,{message:this._("loading"),colSpan:this.headerLength(),className:it(rt("loading"),this.config.className.loading)}),this.props.status===At.Rendered&&this.props.data&&0===this.props.data.length&&w(Xt,{message:this._("noRecordsFound"),colSpan:this.headerLength(),className:it(rt("notfound"),this.config.className.notfound)}),this.props.status===At.Error&&w(Xt,{message:this._("error"),colSpan:this.headerLength(),className:it(rt("error"),this.config.className.error)}))},e}(X),Kt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var r=e.prototype;return r.validateProps=function(){for(var t,e=u(this.props.columns);!(t=e()).done;){var n=t.value;void 0===n.direction&&(n.direction=1),1!==n.direction&&-1!==n.direction&&pt.error("Invalid sort direction "+n.direction)}},r.compare=function(t,e){return t>e?1:t<e?-1:0},r.compareWrapper=function(t,e){for(var n,r=0,i=u(this.props.columns);!(n=i()).done;){var o=n.value;if(0!==r)break;var s=t.cells[o.index].data,a=e.cells[o.index].data;r|="function"==typeof o.compare?o.compare(s,a)*o.direction:this.compare(s,a)*o.direction}return r},r._process=function(t){var e=[].concat(t.rows);e.sort(this.compareWrapper.bind(this));var n=new Q(e);return n.length=t.length,n},n(e,[{key:"type",get:function(){return Y.Sort}}]),e}(et),Yt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var n=e.prototype;return n.getInitialState=function(){return[]},n.handle=function(t,e){"SORT_COLUMN"===t?this.sortColumn(e.index,e.direction,e.multi,e.compare):"SORT_COLUMN_TOGGLE"===t&&this.sortToggle(e.index,e.multi,e.compare)},n.sortToggle=function(t,e,n){var r=[].concat(this.state).find(function(e){return e.index===t});this.sortColumn(t,r&&1===r.direction?-1:1,e,n)},n.sortColumn=function(t,e,n,r){var i=[].concat(this.state),o=i.length,s=i.find(function(e){return e.index===t}),a=!1,u=!1,l=!1,c=!1;if(void 0!==s?n?-1===s.direction?l=!0:c=!0:1===o?c=!0:o>1&&(u=!0,a=!0):0===o?a=!0:o>0&&!n?(a=!0,u=!0):o>0&&n&&(a=!0),u&&(i=[]),a)i.push({index:t,direction:e,compare:r});else if(c){var p=i.indexOf(s);i[p].direction=e}else if(l){var h=i.indexOf(s);i.splice(h,1)}this.setState(i)},e}(st),Zt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var n=e.prototype;return n.sortColumn=function(t,e,n,r){this.dispatch("SORT_COLUMN",{index:t,direction:e,multi:n,compare:r})},n.sortToggle=function(t,e,n){this.dispatch("SORT_COLUMN_TOGGLE",{index:t,multi:e,compare:n})},e}(ut),Jt=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype._process=function(t){var e={};return this.props.url&&(e.url=this.props.url(t.url,this.props.columns)),this.props.body&&(e.body=this.props.body(t.body,this.props.columns)),r({},t,e)},n(e,[{key:"type",get:function(){return Y.ServerSort}}]),e}(et),Qt=/*#__PURE__*/function(t){function e(e,n){var r;return(r=t.call(this,e,n)||this).sortProcessor=void 0,r.actions=void 0,r.store=void 0,r.updateStateFn=void 0,r.updateSortProcessorFn=void 0,r.actions=new Zt(r.config.dispatcher),r.store=new Yt(r.config.dispatcher),e.enabled&&(r.sortProcessor=r.getOrCreateSortProcessor(),r.updateStateFn=r.updateState.bind(s(r)),r.store.on("updated",r.updateStateFn),r.state={direction:0}),r}i(e,t);var n=e.prototype;return n.componentWillUnmount=function(){this.config.pipeline.unregister(this.sortProcessor),this.store.off("updated",this.updateStateFn),this.updateSortProcessorFn&&this.store.off("updated",this.updateSortProcessorFn)},n.updateState=function(){var t=this,e=this.store.state.find(function(e){return e.index===t.props.index});this.setState(e?{direction:e.direction}:{direction:0})},n.updateSortProcessor=function(t){this.sortProcessor.setProps({columns:t})},n.getOrCreateSortProcessor=function(){var t=Y.Sort;this.config.sort&&"object"==typeof this.config.sort.server&&(t=Y.ServerSort);var e,n=this.config.pipeline.getStepsByType(t);return n.length>0?e=n[0]:(this.updateSortProcessorFn=this.updateSortProcessor.bind(this),this.store.on("updated",this.updateSortProcessorFn),e=t===Y.ServerSort?new Jt(r({columns:this.store.state},this.config.sort.server)):new Kt({columns:this.store.state}),this.config.pipeline.register(e)),e},n.changeDirection=function(t){t.preventDefault(),t.stopPropagation(),this.actions.sortToggle(this.props.index,!0===t.shiftKey&&this.config.sort.multiColumn,this.props.compare)},n.render=function(){if(!this.props.enabled)return null;var t=this.state.direction,e="neutral";return 1===t?e="asc":-1===t&&(e="desc"),w("button",{tabIndex:-1,"aria-label":this._("sort.sort"+(1===t?"Desc":"Asc")),title:this._("sort.sort"+(1===t?"Desc":"Asc")),className:it(rt("sort"),rt("sort",e),this.config.className.sort),onClick:this.changeDirection.bind(this)})},e}(X),te=/*#__PURE__*/function(t){function e(){for(var e,n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];return(e=t.call.apply(t,[this].concat(r))||this).moveFn=void 0,e.upFn=void 0,e}i(e,t);var n=e.prototype;return n.getPageX=function(t){return t instanceof MouseEvent?Math.floor(t.pageX):Math.floor(t.changedTouches[0].pageX)},n.start=function(t){var e,n,r,i,o;t.stopPropagation(),this.setState({offsetStart:parseInt(this.props.thRef.current.style.width,10)-this.getPageX(t)}),this.upFn=this.end.bind(this),this.moveFn=(e=this.move.bind(this),void 0===(n=10)&&(n=100),function(){var t=[].slice.call(arguments);r?(clearTimeout(i),i=setTimeout(function(){Date.now()-o>=n&&(e.apply(void 0,t),o=Date.now())},Math.max(n-(Date.now()-o),0))):(e.apply(void 0,t),o=Date.now(),r=!0)}),document.addEventListener("mouseup",this.upFn),document.addEventListener("touchend",this.upFn),document.addEventListener("mousemove",this.moveFn),document.addEventListener("touchmove",this.moveFn)},n.move=function(t){t.stopPropagation();var e=this.props.thRef.current;this.state.offsetStart+this.getPageX(t)>=parseInt(e.style.minWidth,10)&&(e.style.width=this.state.offsetStart+this.getPageX(t)+"px")},n.end=function(t){t.stopPropagation(),document.removeEventListener("mouseup",this.upFn),document.removeEventListener("mousemove",this.moveFn),document.removeEventListener("touchmove",this.moveFn),document.removeEventListener("touchend",this.upFn)},n.render=function(){return w("div",{className:it(rt("th"),rt("resizable")),onMouseDown:this.start.bind(this),onTouchStart:this.start.bind(this),onClick:function(t){return t.stopPropagation()}})},e}(X),ee=/*#__PURE__*/function(t){function e(e,n){var r;return(r=t.call(this,e,n)||this).sortRef={current:null},r.thRef={current:null},r.state={style:{}},r}i(e,t);var n=e.prototype;return n.isSortable=function(){return this.props.column.sort.enabled},n.isResizable=function(){return this.props.column.resizable},n.onClick=function(t){t.stopPropagation(),this.isSortable()&&this.sortRef.current.changeDirection(t)},n.keyDown=function(t){this.isSortable()&&13===t.which&&this.onClick(t)},n.componentDidMount=function(){var t=this;setTimeout(function(){if(t.props.column.fixedHeader&&t.thRef.current){var e=t.thRef.current.offsetTop;"number"==typeof e&&t.setState({style:{top:e}})}},0)},n.content=function(){return void 0!==this.props.column.name?this.props.column.name:void 0!==this.props.column.plugin?w(dt,{pluginId:this.props.column.plugin.id,props:{column:this.props.column}}):null},n.getCustomAttributes=function(){var t=this.props.column;return t?"function"==typeof t.attributes?t.attributes(null,null,this.props.column):t.attributes:{}},n.render=function(){var t={};return this.isSortable()&&(t.tabIndex=0),w("th",r({ref:this.thRef,"data-column-id":this.props.column&&this.props.column.id,className:it(rt("th"),this.isSortable()?rt("th","sort"):null,this.props.column.fixedHeader?rt("th","fixed"):null,this.config.className.th),onClick:this.onClick.bind(this),style:r({},this.config.style.th,{minWidth:this.props.column.minWidth,width:this.props.column.width},this.state.style,this.props.style),onKeyDown:this.keyDown.bind(this),rowSpan:this.props.rowSpan>1?this.props.rowSpan:void 0,colSpan:this.props.colSpan>1?this.props.colSpan:void 0},this.getCustomAttributes(),t),w("div",{className:rt("th","content")},this.content()),this.isSortable()&&w(Qt,r({ref:this.sortRef,index:this.props.index},this.props.column.sort)),this.isResizable()&&this.props.index<this.config.header.visibleColumns.length-1&&w(te,{column:this.props.column,thRef:this.thRef}))},e}(X),ne=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}i(e,t);var n=e.prototype;return n.renderColumn=function(t,e,n,r){var i=function(t,e,n){var r=St.maximumDepth(t),i=n-e;return{rowSpan:Math.floor(i-r-r/i),colSpan:t.columns&&t.columns.length||1}}(t,e,r);return w(ee,{column:t,index:n,colSpan:i.colSpan,rowSpan:i.rowSpan})},n.renderRow=function(t,e,n){var r=this,i=St.leafColumns(this.props.header.columns);return w(Gt,null,t.map(function(t){return t.hidden?null:r.renderColumn(t,e,i.indexOf(t),n)}))},n.renderRows=function(){var t=this,e=St.tabularFormat(this.props.header.columns);return e.map(function(n,r){return t.renderRow(n,r,e.length)})},n.render=function(){return this.props.header?w("thead",{key:this.props.header.id,className:it(rt("thead"),this.config.className.thead)},this.renderRows()):null},e}(X),re=/*#__PURE__*/function(t){function e(){return t.apply(this,arguments)||this}return i(e,t),e.prototype.render=function(){return w("table",{role:"grid",className:it(rt("table"),this.config.className.table),style:r({},this.config.style.table,{height:this.props.height})},w(ne,{header:this.props.header}),w($t,{data:this.props.data,status:this.props.status,header:this.props.header}))},e}(X),ie=/*#__PURE__*/function(e){function n(t,n){var r;return(r=e.call(this,t,n)||this).headerRef={current:null},r.state={isActive:!0},r}i(n,e);var o=n.prototype;return o.componentDidMount=function(){0===this.headerRef.current.children.length&&this.setState({isActive:!1})},o.render=function(){return this.state.isActive?w("div",{ref:this.headerRef,className:it(rt("head"),this.config.className.header),style:r({},this.config.style.header)},w(dt,{position:t.PluginPosition.Header})):null},n}(X),oe=/*#__PURE__*/function(e){function n(t,n){var r;return(r=e.call(this,t,n)||this).footerRef={current:null},r.state={isActive:!0},r}i(n,e);var o=n.prototype;return o.componentDidMount=function(){0===this.footerRef.current.children.length&&this.setState({isActive:!1})},o.render=function(){return this.state.isActive?w("div",{ref:this.footerRef,className:it(rt("footer"),this.config.className.footer),style:r({},this.config.style.footer)},w(dt,{position:t.PluginPosition.Footer})):null},n}(X),se=/*#__PURE__*/function(t){function e(e,n){var r;return(r=t.call(this,e,n)||this).configContext=void 0,r.processPipelineFn=void 0,r.configContext=function(t,e){var n={__c:e="__cC"+_++,__:null,Consumer:function(t,e){return t.children(e)},Provider:function(t){var n,r;return this.getChildContext||(n=[],(r={})[e]=this,this.getChildContext=function(){return r},this.shouldComponentUpdate=function(t){this.props.value!==t.value&&n.some(N)},this.sub=function(t){n.push(t);var e=t.componentWillUnmount;t.componentWillUnmount=function(){n.splice(n.indexOf(t),1),e&&e.call(t)}}),t.children}};return n.Provider.__=n.Consumer.contextType=n}(),r.state={status:At.Loading,header:e.header,data:null},r}i(e,t);var n=e.prototype;return n.processPipeline=function(){try{var t=this;t.props.config.eventEmitter.emit("beforeLoad"),t.setState({status:At.Loading});var e=function(e,n){try{var r=Promise.resolve(t.props.pipeline.process()).then(function(e){t.setState({data:e,status:At.Loaded}),t.props.config.eventEmitter.emit("load",e)})}catch(t){return n(t)}return r&&r.then?r.then(void 0,n):r}(0,function(e){pt.error(e),t.setState({status:At.Error,data:null})});return Promise.resolve(e&&e.then?e.then(function(){}):void 0)}catch(t){return Promise.reject(t)}},n.componentDidMount=function(){try{var t=this,e=t.props.config;return Promise.resolve(t.processPipeline()).then(function(){e.header&&t.state.data&&t.state.data.length&&t.setState({header:e.header.adjustWidth(e)}),t.processPipelineFn=t.processPipeline.bind(t),t.props.pipeline.on("updated",t.processPipelineFn)})}catch(t){return Promise.reject(t)}},n.componentWillUnmount=function(){this.props.pipeline.off("updated",this.processPipelineFn)},n.componentDidUpdate=function(t,e){e.status!=At.Rendered&&this.state.status==At.Loaded&&(this.setState({status:At.Rendered}),this.props.config.eventEmitter.emit("ready"))},n.render=function(){return w(this.configContext.Provider,{value:this.props.config},w("div",{role:"complementary",className:it("gridjs",rt("container"),this.state.status===At.Loading?rt("loading"):null,this.props.config.className.container),style:r({},this.props.config.style.container,{width:this.props.width})},this.state.status===At.Loading&&w("div",{className:rt("loading-bar")}),w(ie,null),w("div",{className:rt("wrapper"),style:{height:this.props.height}},w(re,{ref:this.props.config.tableRef,data:this.state.data,header:this.state.header,width:this.props.width,height:this.props.height,status:this.state.status})),w(oe,null),w("div",{ref:this.props.config.tempRef,id:"gridjs-temp-"+this.props.config.container.id,className:rt("temp")})))},e}(X),ae=/*#__PURE__*/function(t){function e(e){var n;return(n=t.call(this)||this).config=void 0,n.plugin=void 0,n.config=new jt({instance:s(n),eventEmitter:s(n)}).update(e),n.plugin=n.config.plugin,n}i(e,t);var n=e.prototype;return n.updateConfig=function(t){return this.config.update(t),this},n.createElement=function(){return w(se,{config:this.config,pipeline:this.config.pipeline,header:this.config.header,width:this.config.width,height:this.config.height})},n.forceRender=function(){return this.config&&this.config.container||pt.error("Container is empty. Make sure you call render() before forceRender()",!0),this.config.pipeline.clearCache(),B(null,this.config.container),B(this.createElement(),this.config.container),this},n.render=function(t){return t||pt.error("Container element cannot be null",!0),t.childNodes.length>0?(pt.error("The container element "+t+" is not empty. Make sure the container is empty and call render() again"),this):(this.config.container=t,B(this.createElement(),t),this)},e}(tt),ue=0,le=[],ce=[],pe=c.__b,he=c.__r,fe=c.diffed,de=c.__c,_e=c.unmount;function me(t,e){c.__h&&c.__h(Bt,t,ue||e),ue=0;var n=Bt.__H||(Bt.__H={__:[],__h:[]});return t>=n.__.length&&n.__.push({__V:ce}),n.__[t]}function ge(){for(var t;t=le.shift();)if(t.__P&&t.__H)try{t.__H.__h.forEach(ye),t.__H.__h.forEach(be),t.__H.__h=[]}catch(e){t.__H.__h=[],c.__e(e,t.__v)}}c.__b=function(t){Bt=null,pe&&pe(t)},c.__r=function(t){he&&he(t),Wt=0;var e=(Bt=t.__c).__H;e&&(zt===Bt?(e.__h=[],Bt.__h=[],e.__.forEach(function(t){t.__N&&(t.__=t.__N),t.__V=ce,t.__N=t.i=void 0})):(e.__h.forEach(ye),e.__h.forEach(be),e.__h=[])),zt=Bt},c.diffed=function(t){fe&&fe(t);var e=t.__c;e&&e.__H&&(e.__H.__h.length&&(1!==le.push(e)&&qt===c.requestAnimationFrame||((qt=c.requestAnimationFrame)||function(t){var e,n=function(){clearTimeout(r),ve&&cancelAnimationFrame(e),setTimeout(t)},r=setTimeout(n,100);ve&&(e=requestAnimationFrame(n))})(ge)),e.__H.__.forEach(function(t){t.i&&(t.__H=t.i),t.__V!==ce&&(t.__=t.__V),t.i=void 0,t.__V=ce})),zt=Bt=null},c.__c=function(t,e){e.some(function(t){try{t.__h.forEach(ye),t.__h=t.__h.filter(function(t){return!t.__||be(t)})}catch(n){e.some(function(t){t.__h&&(t.__h=[])}),e=[],c.__e(n,t.__v)}}),de&&de(t,e)},c.unmount=function(t){_e&&_e(t);var e,n=t.__c;n&&n.__H&&(n.__H.__.forEach(function(t){try{ye(t)}catch(t){e=t}}),e&&c.__e(e,n.__v))};var ve="function"==typeof requestAnimationFrame;function ye(t){var e=Bt,n=t.__c;"function"==typeof n&&(t.__c=void 0,n()),Bt=e}function be(t){var e=Bt;t.__c=t.__(),Bt=e}function we(t,e){return!t||t.length!==e.length||e.some(function(e,n){return e!==t[n]})}t.BaseActions=ut,t.BaseComponent=X,t.BaseStore=st,t.Cell=Z,t.Component=k,t.Config=jt,t.Dispatcher=kt,t.Grid=ae,t.PluginBaseComponent=ht,t.Row=J,t.className=rt,t.createElement=w,t.createRef=function(){return{current:null}},t.h=w,t.html=K,t.useEffect=function(t,e){var n=me(Wt++,3);!c.__s&&we(n.__H,e)&&(n.__=t,n.i=e,Bt.__H.__h.push(n))},t.useRef=function(t){return ue=5,function(t,e){var n=me(Wt++,7);return we(n.__H,e)?(n.__V=t(),n.i=e,n.__h=t,n.__V):n.__}(function(){return{current:t}},[])}});
//# sourceMappingURL=gridjs.umd.js.map;
/**!

 @license
 handlebars v4.7.7

 Copyright (C) 2011-2019 by Yehuda Katz

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.

 */
!function(a,b){"object"==typeof exports&&"object"==typeof module?module.exports=b():"function"==typeof define&&define.amd?define([],b):"object"==typeof exports?exports.Handlebars=b():a.Handlebars=b()}(this,function(){return function(a){function b(d){if(c[d])return c[d].exports;var e=c[d]={exports:{},id:d,loaded:!1};return a[d].call(e.exports,e,e.exports,b),e.loaded=!0,e.exports}var c={};return b.m=a,b.c=c,b.p="",b(0)}([function(a,b,c){"use strict";function d(){var a=r();return a.compile=function(b,c){return k.compile(b,c,a)},a.precompile=function(b,c){return k.precompile(b,c,a)},a.AST=i["default"],a.Compiler=k.Compiler,a.JavaScriptCompiler=m["default"],a.Parser=j.parser,a.parse=j.parse,a.parseWithoutProcessing=j.parseWithoutProcessing,a}var e=c(1)["default"];b.__esModule=!0;var f=c(2),g=e(f),h=c(45),i=e(h),j=c(46),k=c(51),l=c(52),m=e(l),n=c(49),o=e(n),p=c(44),q=e(p),r=g["default"].create,s=d();s.create=d,q["default"](s),s.Visitor=o["default"],s["default"]=s,b["default"]=s,a.exports=b["default"]},function(a,b){"use strict";b["default"]=function(a){return a&&a.__esModule?a:{"default":a}},b.__esModule=!0},function(a,b,c){"use strict";function d(){var a=new h.HandlebarsEnvironment;return n.extend(a,h),a.SafeString=j["default"],a.Exception=l["default"],a.Utils=n,a.escapeExpression=n.escapeExpression,a.VM=p,a.template=function(b){return p.template(b,a)},a}var e=c(3)["default"],f=c(1)["default"];b.__esModule=!0;var g=c(4),h=e(g),i=c(37),j=f(i),k=c(6),l=f(k),m=c(5),n=e(m),o=c(38),p=e(o),q=c(44),r=f(q),s=d();s.create=d,r["default"](s),s["default"]=s,b["default"]=s,a.exports=b["default"]},function(a,b){"use strict";b["default"]=function(a){if(a&&a.__esModule)return a;var b={};if(null!=a)for(var c in a)Object.prototype.hasOwnProperty.call(a,c)&&(b[c]=a[c]);return b["default"]=a,b},b.__esModule=!0},function(a,b,c){"use strict";function d(a,b,c){this.helpers=a||{},this.partials=b||{},this.decorators=c||{},i.registerDefaultHelpers(this),j.registerDefaultDecorators(this)}var e=c(1)["default"];b.__esModule=!0,b.HandlebarsEnvironment=d;var f=c(5),g=c(6),h=e(g),i=c(10),j=c(30),k=c(32),l=e(k),m=c(33),n="4.7.7";b.VERSION=n;var o=8;b.COMPILER_REVISION=o;var p=7;b.LAST_COMPATIBLE_COMPILER_REVISION=p;var q={1:"<= 1.0.rc.2",2:"== 1.0.0-rc.3",3:"== 1.0.0-rc.4",4:"== 1.x.x",5:"== 2.0.0-alpha.x",6:">= 2.0.0-beta.1",7:">= 4.0.0 <4.3.0",8:">= 4.3.0"};b.REVISION_CHANGES=q;var r="[object Object]";d.prototype={constructor:d,logger:l["default"],log:l["default"].log,registerHelper:function(a,b){if(f.toString.call(a)===r){if(b)throw new h["default"]("Arg not supported with multiple helpers");f.extend(this.helpers,a)}else this.helpers[a]=b},unregisterHelper:function(a){delete this.helpers[a]},registerPartial:function(a,b){if(f.toString.call(a)===r)f.extend(this.partials,a);else{if("undefined"==typeof b)throw new h["default"]('Attempting to register a partial called "'+a+'" as undefined');this.partials[a]=b}},unregisterPartial:function(a){delete this.partials[a]},registerDecorator:function(a,b){if(f.toString.call(a)===r){if(b)throw new h["default"]("Arg not supported with multiple decorators");f.extend(this.decorators,a)}else this.decorators[a]=b},unregisterDecorator:function(a){delete this.decorators[a]},resetLoggedPropertyAccesses:function(){m.resetLoggedProperties()}};var s=l["default"].log;b.log=s,b.createFrame=f.createFrame,b.logger=l["default"]},function(a,b){"use strict";function c(a){return k[a]}function d(a){for(var b=1;b<arguments.length;b++)for(var c in arguments[b])Object.prototype.hasOwnProperty.call(arguments[b],c)&&(a[c]=arguments[b][c]);return a}function e(a,b){for(var c=0,d=a.length;c<d;c++)if(a[c]===b)return c;return-1}function f(a){if("string"!=typeof a){if(a&&a.toHTML)return a.toHTML();if(null==a)return"";if(!a)return a+"";a=""+a}return m.test(a)?a.replace(l,c):a}function g(a){return!a&&0!==a||!(!p(a)||0!==a.length)}function h(a){var b=d({},a);return b._parent=a,b}function i(a,b){return a.path=b,a}function j(a,b){return(a?a+".":"")+b}b.__esModule=!0,b.extend=d,b.indexOf=e,b.escapeExpression=f,b.isEmpty=g,b.createFrame=h,b.blockParams=i,b.appendContextPath=j;var k={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#x27;","`":"&#x60;","=":"&#x3D;"},l=/[&<>"'`=]/g,m=/[&<>"'`=]/,n=Object.prototype.toString;b.toString=n;var o=function(a){return"function"==typeof a};o(/x/)&&(b.isFunction=o=function(a){return"function"==typeof a&&"[object Function]"===n.call(a)}),b.isFunction=o;var p=Array.isArray||function(a){return!(!a||"object"!=typeof a)&&"[object Array]"===n.call(a)};b.isArray=p},function(a,b,c){"use strict";function d(a,b){var c=b&&b.loc,g=void 0,h=void 0,i=void 0,j=void 0;c&&(g=c.start.line,h=c.end.line,i=c.start.column,j=c.end.column,a+=" - "+g+":"+i);for(var k=Error.prototype.constructor.call(this,a),l=0;l<f.length;l++)this[f[l]]=k[f[l]];Error.captureStackTrace&&Error.captureStackTrace(this,d);try{c&&(this.lineNumber=g,this.endLineNumber=h,e?(Object.defineProperty(this,"column",{value:i,enumerable:!0}),Object.defineProperty(this,"endColumn",{value:j,enumerable:!0})):(this.column=i,this.endColumn=j))}catch(m){}}var e=c(7)["default"];b.__esModule=!0;var f=["description","fileName","lineNumber","endLineNumber","message","name","number","stack"];d.prototype=new Error,b["default"]=d,a.exports=b["default"]},function(a,b,c){a.exports={"default":c(8),__esModule:!0}},function(a,b,c){var d=c(9);a.exports=function(a,b,c){return d.setDesc(a,b,c)}},function(a,b){var c=Object;a.exports={create:c.create,getProto:c.getPrototypeOf,isEnum:{}.propertyIsEnumerable,getDesc:c.getOwnPropertyDescriptor,setDesc:c.defineProperty,setDescs:c.defineProperties,getKeys:c.keys,getNames:c.getOwnPropertyNames,getSymbols:c.getOwnPropertySymbols,each:[].forEach}},function(a,b,c){"use strict";function d(a){h["default"](a),j["default"](a),l["default"](a),n["default"](a),p["default"](a),r["default"](a),t["default"](a)}function e(a,b,c){a.helpers[b]&&(a.hooks[b]=a.helpers[b],c||delete a.helpers[b])}var f=c(1)["default"];b.__esModule=!0,b.registerDefaultHelpers=d,b.moveHelperToHooks=e;var g=c(11),h=f(g),i=c(12),j=f(i),k=c(25),l=f(k),m=c(26),n=f(m),o=c(27),p=f(o),q=c(28),r=f(q),s=c(29),t=f(s)},function(a,b,c){"use strict";b.__esModule=!0;var d=c(5);b["default"]=function(a){a.registerHelper("blockHelperMissing",function(b,c){var e=c.inverse,f=c.fn;if(b===!0)return f(this);if(b===!1||null==b)return e(this);if(d.isArray(b))return b.length>0?(c.ids&&(c.ids=[c.name]),a.helpers.each(b,c)):e(this);if(c.data&&c.ids){var g=d.createFrame(c.data);g.contextPath=d.appendContextPath(c.data.contextPath,c.name),c={data:g}}return f(b,c)})},a.exports=b["default"]},function(a,b,c){(function(d){"use strict";var e=c(13)["default"],f=c(1)["default"];b.__esModule=!0;var g=c(5),h=c(6),i=f(h);b["default"]=function(a){a.registerHelper("each",function(a,b){function c(b,c,d){l&&(l.key=b,l.index=c,l.first=0===c,l.last=!!d,m&&(l.contextPath=m+b)),k+=f(a[b],{data:l,blockParams:g.blockParams([a[b],b],[m+b,null])})}if(!b)throw new i["default"]("Must pass iterator to #each");var f=b.fn,h=b.inverse,j=0,k="",l=void 0,m=void 0;if(b.data&&b.ids&&(m=g.appendContextPath(b.data.contextPath,b.ids[0])+"."),g.isFunction(a)&&(a=a.call(this)),b.data&&(l=g.createFrame(b.data)),a&&"object"==typeof a)if(g.isArray(a))for(var n=a.length;j<n;j++)j in a&&c(j,j,j===a.length-1);else if(d.Symbol&&a[d.Symbol.iterator]){for(var o=[],p=a[d.Symbol.iterator](),q=p.next();!q.done;q=p.next())o.push(q.value);a=o;for(var n=a.length;j<n;j++)c(j,j,j===a.length-1)}else!function(){var b=void 0;e(a).forEach(function(a){void 0!==b&&c(b,j-1),b=a,j++}),void 0!==b&&c(b,j-1,!0)}();return 0===j&&(k=h(this)),k})},a.exports=b["default"]}).call(b,function(){return this}())},function(a,b,c){a.exports={"default":c(14),__esModule:!0}},function(a,b,c){c(15),a.exports=c(21).Object.keys},function(a,b,c){var d=c(16);c(18)("keys",function(a){return function(b){return a(d(b))}})},function(a,b,c){var d=c(17);a.exports=function(a){return Object(d(a))}},function(a,b){a.exports=function(a){if(void 0==a)throw TypeError("Can't call method on  "+a);return a}},function(a,b,c){var d=c(19),e=c(21),f=c(24);a.exports=function(a,b){var c=(e.Object||{})[a]||Object[a],g={};g[a]=b(c),d(d.S+d.F*f(function(){c(1)}),"Object",g)}},function(a,b,c){var d=c(20),e=c(21),f=c(22),g="prototype",h=function(a,b,c){var i,j,k,l=a&h.F,m=a&h.G,n=a&h.S,o=a&h.P,p=a&h.B,q=a&h.W,r=m?e:e[b]||(e[b]={}),s=m?d:n?d[b]:(d[b]||{})[g];m&&(c=b);for(i in c)j=!l&&s&&i in s,j&&i in r||(k=j?s[i]:c[i],r[i]=m&&"function"!=typeof s[i]?c[i]:p&&j?f(k,d):q&&s[i]==k?function(a){var b=function(b){return this instanceof a?new a(b):a(b)};return b[g]=a[g],b}(k):o&&"function"==typeof k?f(Function.call,k):k,o&&((r[g]||(r[g]={}))[i]=k))};h.F=1,h.G=2,h.S=4,h.P=8,h.B=16,h.W=32,a.exports=h},function(a,b){var c=a.exports="undefined"!=typeof window&&window.Math==Math?window:"undefined"!=typeof self&&self.Math==Math?self:Function("return this")();"number"==typeof __g&&(__g=c)},function(a,b){var c=a.exports={version:"1.2.6"};"number"==typeof __e&&(__e=c)},function(a,b,c){var d=c(23);a.exports=function(a,b,c){if(d(a),void 0===b)return a;switch(c){case 1:return function(c){return a.call(b,c)};case 2:return function(c,d){return a.call(b,c,d)};case 3:return function(c,d,e){return a.call(b,c,d,e)}}return function(){return a.apply(b,arguments)}}},function(a,b){a.exports=function(a){if("function"!=typeof a)throw TypeError(a+" is not a function!");return a}},function(a,b){a.exports=function(a){try{return!!a()}catch(b){return!0}}},function(a,b,c){"use strict";var d=c(1)["default"];b.__esModule=!0;var e=c(6),f=d(e);b["default"]=function(a){a.registerHelper("helperMissing",function(){if(1!==arguments.length)throw new f["default"]('Missing helper: "'+arguments[arguments.length-1].name+'"')})},a.exports=b["default"]},function(a,b,c){"use strict";var d=c(1)["default"];b.__esModule=!0;var e=c(5),f=c(6),g=d(f);b["default"]=function(a){a.registerHelper("if",function(a,b){if(2!=arguments.length)throw new g["default"]("#if requires exactly one argument");return e.isFunction(a)&&(a=a.call(this)),!b.hash.includeZero&&!a||e.isEmpty(a)?b.inverse(this):b.fn(this)}),a.registerHelper("unless",function(b,c){if(2!=arguments.length)throw new g["default"]("#unless requires exactly one argument");return a.helpers["if"].call(this,b,{fn:c.inverse,inverse:c.fn,hash:c.hash})})},a.exports=b["default"]},function(a,b){"use strict";b.__esModule=!0,b["default"]=function(a){a.registerHelper("log",function(){for(var b=[void 0],c=arguments[arguments.length-1],d=0;d<arguments.length-1;d++)b.push(arguments[d]);var e=1;null!=c.hash.level?e=c.hash.level:c.data&&null!=c.data.level&&(e=c.data.level),b[0]=e,a.log.apply(a,b)})},a.exports=b["default"]},function(a,b){"use strict";b.__esModule=!0,b["default"]=function(a){a.registerHelper("lookup",function(a,b,c){return a?c.lookupProperty(a,b):a})},a.exports=b["default"]},function(a,b,c){"use strict";var d=c(1)["default"];b.__esModule=!0;var e=c(5),f=c(6),g=d(f);b["default"]=function(a){a.registerHelper("with",function(a,b){if(2!=arguments.length)throw new g["default"]("#with requires exactly one argument");e.isFunction(a)&&(a=a.call(this));var c=b.fn;if(e.isEmpty(a))return b.inverse(this);var d=b.data;return b.data&&b.ids&&(d=e.createFrame(b.data),d.contextPath=e.appendContextPath(b.data.contextPath,b.ids[0])),c(a,{data:d,blockParams:e.blockParams([a],[d&&d.contextPath])})})},a.exports=b["default"]},function(a,b,c){"use strict";function d(a){g["default"](a)}var e=c(1)["default"];b.__esModule=!0,b.registerDefaultDecorators=d;var f=c(31),g=e(f)},function(a,b,c){"use strict";b.__esModule=!0;var d=c(5);b["default"]=function(a){a.registerDecorator("inline",function(a,b,c,e){var f=a;return b.partials||(b.partials={},f=function(e,f){var g=c.partials;c.partials=d.extend({},g,b.partials);var h=a(e,f);return c.partials=g,h}),b.partials[e.args[0]]=e.fn,f})},a.exports=b["default"]},function(a,b,c){"use strict";b.__esModule=!0;var d=c(5),e={methodMap:["debug","info","warn","error"],level:"info",lookupLevel:function(a){if("string"==typeof a){var b=d.indexOf(e.methodMap,a.toLowerCase());a=b>=0?b:parseInt(a,10)}return a},log:function(a){if(a=e.lookupLevel(a),"undefined"!=typeof console&&e.lookupLevel(e.level)<=a){var b=e.methodMap[a];console[b]||(b="log");for(var c=arguments.length,d=Array(c>1?c-1:0),f=1;f<c;f++)d[f-1]=arguments[f];console[b].apply(console,d)}}};b["default"]=e,a.exports=b["default"]},function(a,b,c){"use strict";function d(a){var b=i(null);b.constructor=!1,b.__defineGetter__=!1,b.__defineSetter__=!1,b.__lookupGetter__=!1;var c=i(null);return c.__proto__=!1,{properties:{whitelist:l.createNewLookupObject(c,a.allowedProtoProperties),defaultValue:a.allowProtoPropertiesByDefault},methods:{whitelist:l.createNewLookupObject(b,a.allowedProtoMethods),defaultValue:a.allowProtoMethodsByDefault}}}function e(a,b,c){return"function"==typeof a?f(b.methods,c):f(b.properties,c)}function f(a,b){return void 0!==a.whitelist[b]?a.whitelist[b]===!0:void 0!==a.defaultValue?a.defaultValue:(g(b),!1)}function g(a){o[a]!==!0&&(o[a]=!0,n.log("error",'Handlebars: Access has been denied to resolve the property "'+a+'" because it is not an "own property" of its parent.\nYou can add a runtime option to disable the check or this warning:\nSee https://handlebarsjs.com/api-reference/runtime-options.html#options-to-control-prototype-access for details'))}function h(){j(o).forEach(function(a){delete o[a]})}var i=c(34)["default"],j=c(13)["default"],k=c(3)["default"];b.__esModule=!0,b.createProtoAccessControl=d,b.resultIsAllowed=e,b.resetLoggedProperties=h;var l=c(36),m=c(32),n=k(m),o=i(null)},function(a,b,c){a.exports={"default":c(35),__esModule:!0}},function(a,b,c){var d=c(9);a.exports=function(a,b){return d.create(a,b)}},function(a,b,c){"use strict";function d(){for(var a=arguments.length,b=Array(a),c=0;c<a;c++)b[c]=arguments[c];return f.extend.apply(void 0,[e(null)].concat(b))}var e=c(34)["default"];b.__esModule=!0,b.createNewLookupObject=d;var f=c(5)},function(a,b){"use strict";function c(a){this.string=a}b.__esModule=!0,c.prototype.toString=c.prototype.toHTML=function(){return""+this.string},b["default"]=c,a.exports=b["default"]},function(a,b,c){"use strict";function d(a){var b=a&&a[0]||1,c=v.COMPILER_REVISION;if(!(b>=v.LAST_COMPATIBLE_COMPILER_REVISION&&b<=v.COMPILER_REVISION)){if(b<v.LAST_COMPATIBLE_COMPILER_REVISION){var d=v.REVISION_CHANGES[c],e=v.REVISION_CHANGES[b];throw new u["default"]("Template was precompiled with an older version of Handlebars than the current runtime. Please update your precompiler to a newer version ("+d+") or downgrade your runtime to an older version ("+e+").")}throw new u["default"]("Template was precompiled with a newer version of Handlebars than the current runtime. Please update your runtime to a newer version ("+a[1]+").")}}function e(a,b){function c(c,d,e){e.hash&&(d=s.extend({},d,e.hash),e.ids&&(e.ids[0]=!0)),c=b.VM.resolvePartial.call(this,c,d,e);var f=s.extend({},e,{hooks:this.hooks,protoAccessControl:this.protoAccessControl}),g=b.VM.invokePartial.call(this,c,d,f);if(null==g&&b.compile&&(e.partials[e.name]=b.compile(c,a.compilerOptions,b),g=e.partials[e.name](d,f)),null!=g){if(e.indent){for(var h=g.split("\n"),i=0,j=h.length;i<j&&(h[i]||i+1!==j);i++)h[i]=e.indent+h[i];g=h.join("\n")}return g}throw new u["default"]("The partial "+e.name+" could not be compiled when running in runtime-only mode")}function d(b){function c(b){return""+a.main(g,b,g.helpers,g.partials,f,i,h)}var e=arguments.length<=1||void 0===arguments[1]?{}:arguments[1],f=e.data;d._setup(e),!e.partial&&a.useData&&(f=j(b,f));var h=void 0,i=a.useBlockParams?[]:void 0;return a.useDepths&&(h=e.depths?b!=e.depths[0]?[b].concat(e.depths):e.depths:[b]),(c=k(a.main,c,g,e.depths||[],f,i))(b,e)}if(!b)throw new u["default"]("No environment passed to template");if(!a||!a.main)throw new u["default"]("Unknown template object: "+typeof a);a.main.decorator=a.main_d,b.VM.checkRevision(a.compiler);var e=a.compiler&&7===a.compiler[0],g={strict:function(a,b,c){if(!(a&&b in a))throw new u["default"]('"'+b+'" not defined in '+a,{loc:c});return g.lookupProperty(a,b)},lookupProperty:function(a,b){var c=a[b];return null==c?c:Object.prototype.hasOwnProperty.call(a,b)?c:y.resultIsAllowed(c,g.protoAccessControl,b)?c:void 0},lookup:function(a,b){for(var c=a.length,d=0;d<c;d++){var e=a[d]&&g.lookupProperty(a[d],b);if(null!=e)return a[d][b]}},lambda:function(a,b){return"function"==typeof a?a.call(b):a},escapeExpression:s.escapeExpression,invokePartial:c,fn:function(b){var c=a[b];return c.decorator=a[b+"_d"],c},programs:[],program:function(a,b,c,d,e){var g=this.programs[a],h=this.fn(a);return b||e||d||c?g=f(this,a,h,b,c,d,e):g||(g=this.programs[a]=f(this,a,h)),g},data:function(a,b){for(;a&&b--;)a=a._parent;return a},mergeIfNeeded:function(a,b){var c=a||b;return a&&b&&a!==b&&(c=s.extend({},b,a)),c},nullContext:n({}),noop:b.VM.noop,compilerInfo:a.compiler};return d.isTop=!0,d._setup=function(c){if(c.partial)g.protoAccessControl=c.protoAccessControl,g.helpers=c.helpers,g.partials=c.partials,g.decorators=c.decorators,g.hooks=c.hooks;else{var d=s.extend({},b.helpers,c.helpers);l(d,g),g.helpers=d,a.usePartial&&(g.partials=g.mergeIfNeeded(c.partials,b.partials)),(a.usePartial||a.useDecorators)&&(g.decorators=s.extend({},b.decorators,c.decorators)),g.hooks={},g.protoAccessControl=y.createProtoAccessControl(c);var f=c.allowCallsToHelperMissing||e;w.moveHelperToHooks(g,"helperMissing",f),w.moveHelperToHooks(g,"blockHelperMissing",f)}},d._child=function(b,c,d,e){if(a.useBlockParams&&!d)throw new u["default"]("must pass block params");if(a.useDepths&&!e)throw new u["default"]("must pass parent depths");return f(g,b,a[b],c,0,d,e)},d}function f(a,b,c,d,e,f,g){function h(b){var e=arguments.length<=1||void 0===arguments[1]?{}:arguments[1],h=g;return!g||b==g[0]||b===a.nullContext&&null===g[0]||(h=[b].concat(g)),c(a,b,a.helpers,a.partials,e.data||d,f&&[e.blockParams].concat(f),h)}return h=k(c,h,a,g,d,f),h.program=b,h.depth=g?g.length:0,h.blockParams=e||0,h}function g(a,b,c){return a?a.call||c.name||(c.name=a,a=c.partials[a]):a="@partial-block"===c.name?c.data["partial-block"]:c.partials[c.name],a}function h(a,b,c){var d=c.data&&c.data["partial-block"];c.partial=!0,c.ids&&(c.data.contextPath=c.ids[0]||c.data.contextPath);var e=void 0;if(c.fn&&c.fn!==i&&!function(){c.data=v.createFrame(c.data);var a=c.fn;e=c.data["partial-block"]=function(b){var c=arguments.length<=1||void 0===arguments[1]?{}:arguments[1];return c.data=v.createFrame(c.data),c.data["partial-block"]=d,a(b,c)},a.partials&&(c.partials=s.extend({},c.partials,a.partials))}(),void 0===a&&e&&(a=e),void 0===a)throw new u["default"]("The partial "+c.name+" could not be found");if(a instanceof Function)return a(b,c)}function i(){return""}function j(a,b){return b&&"root"in b||(b=b?v.createFrame(b):{},b.root=a),b}function k(a,b,c,d,e,f){if(a.decorator){var g={};b=a.decorator(b,g,c,d&&d[0],e,f,d),s.extend(b,g)}return b}function l(a,b){o(a).forEach(function(c){var d=a[c];a[c]=m(d,b)})}function m(a,b){var c=b.lookupProperty;return x.wrapHelper(a,function(a){return s.extend({lookupProperty:c},a)})}var n=c(39)["default"],o=c(13)["default"],p=c(3)["default"],q=c(1)["default"];b.__esModule=!0,b.checkRevision=d,b.template=e,b.wrapProgram=f,b.resolvePartial=g,b.invokePartial=h,b.noop=i;var r=c(5),s=p(r),t=c(6),u=q(t),v=c(4),w=c(10),x=c(43),y=c(33)},function(a,b,c){a.exports={"default":c(40),__esModule:!0}},function(a,b,c){c(41),a.exports=c(21).Object.seal},function(a,b,c){var d=c(42);c(18)("seal",function(a){return function(b){return a&&d(b)?a(b):b}})},function(a,b){a.exports=function(a){return"object"==typeof a?null!==a:"function"==typeof a}},function(a,b){"use strict";function c(a,b){if("function"!=typeof a)return a;var c=function(){var c=arguments[arguments.length-1];return arguments[arguments.length-1]=b(c),a.apply(this,arguments)};return c}b.__esModule=!0,b.wrapHelper=c},function(a,b){(function(c){"use strict";b.__esModule=!0,b["default"]=function(a){var b="undefined"!=typeof c?c:window,d=b.Handlebars;a.noConflict=function(){return b.Handlebars===a&&(b.Handlebars=d),a}},a.exports=b["default"]}).call(b,function(){return this}())},function(a,b){"use strict";b.__esModule=!0;var c={helpers:{helperExpression:function(a){return"SubExpression"===a.type||("MustacheStatement"===a.type||"BlockStatement"===a.type)&&!!(a.params&&a.params.length||a.hash)},scopedId:function(a){return/^\.|this\b/.test(a.original)},simpleId:function(a){return 1===a.parts.length&&!c.helpers.scopedId(a)&&!a.depth}}};b["default"]=c,a.exports=b["default"]},function(a,b,c){"use strict";function d(a,b){if("Program"===a.type)return a;i["default"].yy=o,o.locInfo=function(a){return new o.SourceLocation(b&&b.srcName,a)};var c=i["default"].parse(a);return c}function e(a,b){var c=d(a,b),e=new k["default"](b);return e.accept(c)}var f=c(1)["default"],g=c(3)["default"];b.__esModule=!0,b.parseWithoutProcessing=d,b.parse=e;var h=c(47),i=f(h),j=c(48),k=f(j),l=c(50),m=g(l),n=c(5);b.parser=i["default"];var o={};n.extend(o,m)},function(a,b){"use strict";b.__esModule=!0;var c=function(){function a(){this.yy={}}var b={trace:function(){},yy:{},symbols_:{error:2,root:3,program:4,EOF:5,program_repetition0:6,statement:7,mustache:8,block:9,rawBlock:10,partial:11,partialBlock:12,content:13,COMMENT:14,CONTENT:15,openRawBlock:16,rawBlock_repetition0:17,END_RAW_BLOCK:18,OPEN_RAW_BLOCK:19,helperName:20,openRawBlock_repetition0:21,openRawBlock_option0:22,CLOSE_RAW_BLOCK:23,openBlock:24,block_option0:25,closeBlock:26,openInverse:27,block_option1:28,OPEN_BLOCK:29,openBlock_repetition0:30,openBlock_option0:31,openBlock_option1:32,CLOSE:33,OPEN_INVERSE:34,openInverse_repetition0:35,openInverse_option0:36,openInverse_option1:37,openInverseChain:38,OPEN_INVERSE_CHAIN:39,openInverseChain_repetition0:40,openInverseChain_option0:41,openInverseChain_option1:42,inverseAndProgram:43,INVERSE:44,inverseChain:45,inverseChain_option0:46,OPEN_ENDBLOCK:47,OPEN:48,mustache_repetition0:49,mustache_option0:50,OPEN_UNESCAPED:51,mustache_repetition1:52,mustache_option1:53,CLOSE_UNESCAPED:54,OPEN_PARTIAL:55,partialName:56,partial_repetition0:57,partial_option0:58,openPartialBlock:59,OPEN_PARTIAL_BLOCK:60,openPartialBlock_repetition0:61,openPartialBlock_option0:62,param:63,sexpr:64,OPEN_SEXPR:65,sexpr_repetition0:66,sexpr_option0:67,CLOSE_SEXPR:68,hash:69,hash_repetition_plus0:70,hashSegment:71,ID:72,EQUALS:73,blockParams:74,OPEN_BLOCK_PARAMS:75,blockParams_repetition_plus0:76,CLOSE_BLOCK_PARAMS:77,path:78,dataName:79,STRING:80,NUMBER:81,BOOLEAN:82,UNDEFINED:83,NULL:84,DATA:85,pathSegments:86,SEP:87,$accept:0,$end:1},terminals_:{2:"error",5:"EOF",14:"COMMENT",15:"CONTENT",18:"END_RAW_BLOCK",19:"OPEN_RAW_BLOCK",23:"CLOSE_RAW_BLOCK",29:"OPEN_BLOCK",33:"CLOSE",34:"OPEN_INVERSE",39:"OPEN_INVERSE_CHAIN",44:"INVERSE",47:"OPEN_ENDBLOCK",48:"OPEN",51:"OPEN_UNESCAPED",54:"CLOSE_UNESCAPED",55:"OPEN_PARTIAL",60:"OPEN_PARTIAL_BLOCK",65:"OPEN_SEXPR",68:"CLOSE_SEXPR",72:"ID",73:"EQUALS",75:"OPEN_BLOCK_PARAMS",77:"CLOSE_BLOCK_PARAMS",80:"STRING",81:"NUMBER",82:"BOOLEAN",83:"UNDEFINED",84:"NULL",85:"DATA",87:"SEP"},productions_:[0,[3,2],[4,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[13,1],[10,3],[16,5],[9,4],[9,4],[24,6],[27,6],[38,6],[43,2],[45,3],[45,1],[26,3],[8,5],[8,5],[11,5],[12,3],[59,5],[63,1],[63,1],[64,5],[69,1],[71,3],[74,3],[20,1],[20,1],[20,1],[20,1],[20,1],[20,1],[20,1],[56,1],[56,1],[79,2],[78,1],[86,3],[86,1],[6,0],[6,2],[17,0],[17,2],[21,0],[21,2],[22,0],[22,1],[25,0],[25,1],[28,0],[28,1],[30,0],[30,2],[31,0],[31,1],[32,0],[32,1],[35,0],[35,2],[36,0],[36,1],[37,0],[37,1],[40,0],[40,2],[41,0],[41,1],[42,0],[42,1],[46,0],[46,1],[49,0],[49,2],[50,0],[50,1],[52,0],[52,2],[53,0],[53,1],[57,0],[57,2],[58,0],[58,1],[61,0],[61,2],[62,0],[62,1],[66,0],[66,2],[67,0],[67,1],[70,1],[70,2],[76,1],[76,2]],performAction:function(a,b,c,d,e,f,g){var h=f.length-1;switch(e){case 1:return f[h-1];case 2:this.$=d.prepareProgram(f[h]);break;case 3:this.$=f[h];break;case 4:this.$=f[h];break;case 5:this.$=f[h];break;case 6:this.$=f[h];break;case 7:this.$=f[h];break;case 8:this.$=f[h];break;case 9:this.$={type:"CommentStatement",value:d.stripComment(f[h]),strip:d.stripFlags(f[h],f[h]),loc:d.locInfo(this._$)};break;case 10:this.$={type:"ContentStatement",original:f[h],value:f[h],loc:d.locInfo(this._$)};break;case 11:this.$=d.prepareRawBlock(f[h-2],f[h-1],f[h],this._$);break;case 12:this.$={path:f[h-3],params:f[h-2],hash:f[h-1]};break;case 13:this.$=d.prepareBlock(f[h-3],f[h-2],f[h-1],f[h],!1,this._$);break;case 14:this.$=d.prepareBlock(f[h-3],f[h-2],f[h-1],f[h],!0,this._$);break;case 15:this.$={open:f[h-5],path:f[h-4],params:f[h-3],hash:f[h-2],blockParams:f[h-1],strip:d.stripFlags(f[h-5],f[h])};break;case 16:this.$={path:f[h-4],params:f[h-3],hash:f[h-2],blockParams:f[h-1],strip:d.stripFlags(f[h-5],f[h])};break;case 17:this.$={path:f[h-4],params:f[h-3],hash:f[h-2],blockParams:f[h-1],strip:d.stripFlags(f[h-5],f[h])};break;case 18:this.$={strip:d.stripFlags(f[h-1],f[h-1]),program:f[h]};break;case 19:var i=d.prepareBlock(f[h-2],f[h-1],f[h],f[h],!1,this._$),j=d.prepareProgram([i],f[h-1].loc);j.chained=!0,this.$={strip:f[h-2].strip,program:j,chain:!0};break;case 20:this.$=f[h];break;case 21:this.$={path:f[h-1],strip:d.stripFlags(f[h-2],f[h])};break;case 22:this.$=d.prepareMustache(f[h-3],f[h-2],f[h-1],f[h-4],d.stripFlags(f[h-4],f[h]),this._$);break;case 23:this.$=d.prepareMustache(f[h-3],f[h-2],f[h-1],f[h-4],d.stripFlags(f[h-4],f[h]),this._$);break;case 24:this.$={type:"PartialStatement",name:f[h-3],params:f[h-2],hash:f[h-1],indent:"",strip:d.stripFlags(f[h-4],f[h]),loc:d.locInfo(this._$)};break;case 25:this.$=d.preparePartialBlock(f[h-2],f[h-1],f[h],this._$);break;case 26:this.$={path:f[h-3],params:f[h-2],hash:f[h-1],strip:d.stripFlags(f[h-4],f[h])};break;case 27:this.$=f[h];break;case 28:this.$=f[h];break;case 29:this.$={type:"SubExpression",path:f[h-3],params:f[h-2],hash:f[h-1],loc:d.locInfo(this._$)};break;case 30:this.$={type:"Hash",pairs:f[h],loc:d.locInfo(this._$)};break;case 31:this.$={type:"HashPair",key:d.id(f[h-2]),value:f[h],loc:d.locInfo(this._$)};break;case 32:this.$=d.id(f[h-1]);break;case 33:this.$=f[h];break;case 34:this.$=f[h];break;case 35:this.$={type:"StringLiteral",value:f[h],original:f[h],loc:d.locInfo(this._$)};break;case 36:this.$={type:"NumberLiteral",value:Number(f[h]),original:Number(f[h]),loc:d.locInfo(this._$)};break;case 37:this.$={type:"BooleanLiteral",value:"true"===f[h],original:"true"===f[h],loc:d.locInfo(this._$)};break;case 38:this.$={type:"UndefinedLiteral",original:void 0,value:void 0,loc:d.locInfo(this._$)};break;case 39:this.$={type:"NullLiteral",original:null,value:null,loc:d.locInfo(this._$)};break;case 40:this.$=f[h];break;case 41:this.$=f[h];break;case 42:this.$=d.preparePath(!0,f[h],this._$);break;case 43:this.$=d.preparePath(!1,f[h],this._$);break;case 44:f[h-2].push({part:d.id(f[h]),original:f[h],separator:f[h-1]}),this.$=f[h-2];break;case 45:this.$=[{part:d.id(f[h]),original:f[h]}];break;case 46:this.$=[];break;case 47:f[h-1].push(f[h]);break;case 48:this.$=[];break;case 49:f[h-1].push(f[h]);break;case 50:this.$=[];break;case 51:f[h-1].push(f[h]);break;case 58:this.$=[];break;case 59:f[h-1].push(f[h]);break;case 64:this.$=[];break;case 65:f[h-1].push(f[h]);break;case 70:this.$=[];break;case 71:f[h-1].push(f[h]);break;case 78:this.$=[];break;case 79:f[h-1].push(f[h]);break;case 82:this.$=[];break;case 83:f[h-1].push(f[h]);break;case 86:this.$=[];break;case 87:f[h-1].push(f[h]);break;case 90:this.$=[];break;case 91:f[h-1].push(f[h]);break;case 94:this.$=[];break;case 95:f[h-1].push(f[h]);break;case 98:this.$=[f[h]];break;case 99:f[h-1].push(f[h]);break;case 100:this.$=[f[h]];break;case 101:f[h-1].push(f[h])}},table:[{3:1,4:2,5:[2,46],6:3,14:[2,46],15:[2,46],19:[2,46],29:[2,46],34:[2,46],48:[2,46],51:[2,46],55:[2,46],60:[2,46]},{1:[3]},{5:[1,4]},{5:[2,2],7:5,8:6,9:7,10:8,11:9,12:10,13:11,14:[1,12],15:[1,20],16:17,19:[1,23],24:15,27:16,29:[1,21],34:[1,22],39:[2,2],44:[2,2],47:[2,2],48:[1,13],51:[1,14],55:[1,18],59:19,60:[1,24]},{1:[2,1]},{5:[2,47],14:[2,47],15:[2,47],19:[2,47],29:[2,47],34:[2,47],39:[2,47],44:[2,47],47:[2,47],48:[2,47],51:[2,47],55:[2,47],60:[2,47]},{5:[2,3],14:[2,3],15:[2,3],19:[2,3],29:[2,3],34:[2,3],39:[2,3],44:[2,3],47:[2,3],48:[2,3],51:[2,3],55:[2,3],60:[2,3]},{5:[2,4],14:[2,4],15:[2,4],19:[2,4],29:[2,4],34:[2,4],39:[2,4],44:[2,4],47:[2,4],48:[2,4],51:[2,4],55:[2,4],60:[2,4]},{5:[2,5],14:[2,5],15:[2,5],19:[2,5],29:[2,5],34:[2,5],39:[2,5],44:[2,5],47:[2,5],48:[2,5],51:[2,5],55:[2,5],60:[2,5]},{5:[2,6],14:[2,6],15:[2,6],19:[2,6],29:[2,6],34:[2,6],39:[2,6],44:[2,6],47:[2,6],48:[2,6],51:[2,6],55:[2,6],60:[2,6]},{5:[2,7],14:[2,7],15:[2,7],19:[2,7],29:[2,7],34:[2,7],39:[2,7],44:[2,7],47:[2,7],48:[2,7],51:[2,7],55:[2,7],60:[2,7]},{5:[2,8],14:[2,8],15:[2,8],19:[2,8],29:[2,8],34:[2,8],39:[2,8],44:[2,8],47:[2,8],48:[2,8],51:[2,8],55:[2,8],60:[2,8]},{5:[2,9],14:[2,9],15:[2,9],19:[2,9],29:[2,9],34:[2,9],39:[2,9],44:[2,9],47:[2,9],48:[2,9],51:[2,9],55:[2,9],60:[2,9]},{20:25,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:36,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{4:37,6:3,14:[2,46],15:[2,46],19:[2,46],29:[2,46],34:[2,46],39:[2,46],44:[2,46],47:[2,46],48:[2,46],51:[2,46],55:[2,46],60:[2,46]},{4:38,6:3,14:[2,46],15:[2,46],19:[2,46],29:[2,46],34:[2,46],44:[2,46],47:[2,46],48:[2,46],51:[2,46],55:[2,46],60:[2,46]},{15:[2,48],17:39,18:[2,48]},{20:41,56:40,64:42,65:[1,43],72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{4:44,6:3,14:[2,46],15:[2,46],19:[2,46],29:[2,46],34:[2,46],47:[2,46],48:[2,46],51:[2,46],55:[2,46],60:[2,46]},{5:[2,10],14:[2,10],15:[2,10],18:[2,10],19:[2,10],29:[2,10],34:[2,10],39:[2,10],44:[2,10],47:[2,10],48:[2,10],51:[2,10],55:[2,10],60:[2,10]},{20:45,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:46,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:47,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:41,56:48,64:42,65:[1,43],72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{33:[2,78],49:49,65:[2,78],72:[2,78],80:[2,78],81:[2,78],82:[2,78],83:[2,78],84:[2,78],85:[2,78]},{23:[2,33],33:[2,33],54:[2,33],65:[2,33],68:[2,33],72:[2,33],75:[2,33],80:[2,33],81:[2,33],82:[2,33],83:[2,33],84:[2,33],85:[2,33]},{23:[2,34],33:[2,34],54:[2,34],65:[2,34],68:[2,34],72:[2,34],75:[2,34],80:[2,34],81:[2,34],82:[2,34],83:[2,34],84:[2,34],85:[2,34]},{23:[2,35],33:[2,35],54:[2,35],65:[2,35],68:[2,35],72:[2,35],75:[2,35],80:[2,35],81:[2,35],82:[2,35],83:[2,35],84:[2,35],85:[2,35]},{23:[2,36],33:[2,36],54:[2,36],65:[2,36],68:[2,36],72:[2,36],75:[2,36],80:[2,36],81:[2,36],82:[2,36],83:[2,36],84:[2,36],85:[2,36]},{23:[2,37],33:[2,37],54:[2,37],65:[2,37],68:[2,37],72:[2,37],75:[2,37],80:[2,37],81:[2,37],82:[2,37],83:[2,37],84:[2,37],85:[2,37]},{23:[2,38],33:[2,38],54:[2,38],65:[2,38],68:[2,38],72:[2,38],75:[2,38],80:[2,38],81:[2,38],82:[2,38],83:[2,38],84:[2,38],85:[2,38]},{23:[2,39],33:[2,39],54:[2,39],65:[2,39],68:[2,39],72:[2,39],75:[2,39],80:[2,39],81:[2,39],82:[2,39],83:[2,39],84:[2,39],85:[2,39]},{23:[2,43],33:[2,43],54:[2,43],65:[2,43],68:[2,43],72:[2,43],75:[2,43],80:[2,43],81:[2,43],82:[2,43],83:[2,43],84:[2,43],85:[2,43],87:[1,50]},{72:[1,35],86:51},{23:[2,45],33:[2,45],54:[2,45],65:[2,45],68:[2,45],72:[2,45],75:[2,45],80:[2,45],81:[2,45],82:[2,45],83:[2,45],84:[2,45],85:[2,45],87:[2,45]},{52:52,54:[2,82],65:[2,82],72:[2,82],80:[2,82],81:[2,82],82:[2,82],83:[2,82],84:[2,82],85:[2,82]},{25:53,38:55,39:[1,57],43:56,44:[1,58],45:54,47:[2,54]},{28:59,43:60,44:[1,58],47:[2,56]},{13:62,15:[1,20],18:[1,61]},{33:[2,86],57:63,65:[2,86],72:[2,86],80:[2,86],81:[2,86],82:[2,86],83:[2,86],84:[2,86],85:[2,86]},{33:[2,40],65:[2,40],72:[2,40],80:[2,40],81:[2,40],82:[2,40],83:[2,40],84:[2,40],85:[2,40]},{
        33:[2,41],65:[2,41],72:[2,41],80:[2,41],81:[2,41],82:[2,41],83:[2,41],84:[2,41],85:[2,41]},{20:64,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{26:65,47:[1,66]},{30:67,33:[2,58],65:[2,58],72:[2,58],75:[2,58],80:[2,58],81:[2,58],82:[2,58],83:[2,58],84:[2,58],85:[2,58]},{33:[2,64],35:68,65:[2,64],72:[2,64],75:[2,64],80:[2,64],81:[2,64],82:[2,64],83:[2,64],84:[2,64],85:[2,64]},{21:69,23:[2,50],65:[2,50],72:[2,50],80:[2,50],81:[2,50],82:[2,50],83:[2,50],84:[2,50],85:[2,50]},{33:[2,90],61:70,65:[2,90],72:[2,90],80:[2,90],81:[2,90],82:[2,90],83:[2,90],84:[2,90],85:[2,90]},{20:74,33:[2,80],50:71,63:72,64:75,65:[1,43],69:73,70:76,71:77,72:[1,78],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{72:[1,79]},{23:[2,42],33:[2,42],54:[2,42],65:[2,42],68:[2,42],72:[2,42],75:[2,42],80:[2,42],81:[2,42],82:[2,42],83:[2,42],84:[2,42],85:[2,42],87:[1,50]},{20:74,53:80,54:[2,84],63:81,64:75,65:[1,43],69:82,70:76,71:77,72:[1,78],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{26:83,47:[1,66]},{47:[2,55]},{4:84,6:3,14:[2,46],15:[2,46],19:[2,46],29:[2,46],34:[2,46],39:[2,46],44:[2,46],47:[2,46],48:[2,46],51:[2,46],55:[2,46],60:[2,46]},{47:[2,20]},{20:85,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{4:86,6:3,14:[2,46],15:[2,46],19:[2,46],29:[2,46],34:[2,46],47:[2,46],48:[2,46],51:[2,46],55:[2,46],60:[2,46]},{26:87,47:[1,66]},{47:[2,57]},{5:[2,11],14:[2,11],15:[2,11],19:[2,11],29:[2,11],34:[2,11],39:[2,11],44:[2,11],47:[2,11],48:[2,11],51:[2,11],55:[2,11],60:[2,11]},{15:[2,49],18:[2,49]},{20:74,33:[2,88],58:88,63:89,64:75,65:[1,43],69:90,70:76,71:77,72:[1,78],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{65:[2,94],66:91,68:[2,94],72:[2,94],80:[2,94],81:[2,94],82:[2,94],83:[2,94],84:[2,94],85:[2,94]},{5:[2,25],14:[2,25],15:[2,25],19:[2,25],29:[2,25],34:[2,25],39:[2,25],44:[2,25],47:[2,25],48:[2,25],51:[2,25],55:[2,25],60:[2,25]},{20:92,72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:74,31:93,33:[2,60],63:94,64:75,65:[1,43],69:95,70:76,71:77,72:[1,78],75:[2,60],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:74,33:[2,66],36:96,63:97,64:75,65:[1,43],69:98,70:76,71:77,72:[1,78],75:[2,66],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:74,22:99,23:[2,52],63:100,64:75,65:[1,43],69:101,70:76,71:77,72:[1,78],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{20:74,33:[2,92],62:102,63:103,64:75,65:[1,43],69:104,70:76,71:77,72:[1,78],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{33:[1,105]},{33:[2,79],65:[2,79],72:[2,79],80:[2,79],81:[2,79],82:[2,79],83:[2,79],84:[2,79],85:[2,79]},{33:[2,81]},{23:[2,27],33:[2,27],54:[2,27],65:[2,27],68:[2,27],72:[2,27],75:[2,27],80:[2,27],81:[2,27],82:[2,27],83:[2,27],84:[2,27],85:[2,27]},{23:[2,28],33:[2,28],54:[2,28],65:[2,28],68:[2,28],72:[2,28],75:[2,28],80:[2,28],81:[2,28],82:[2,28],83:[2,28],84:[2,28],85:[2,28]},{23:[2,30],33:[2,30],54:[2,30],68:[2,30],71:106,72:[1,107],75:[2,30]},{23:[2,98],33:[2,98],54:[2,98],68:[2,98],72:[2,98],75:[2,98]},{23:[2,45],33:[2,45],54:[2,45],65:[2,45],68:[2,45],72:[2,45],73:[1,108],75:[2,45],80:[2,45],81:[2,45],82:[2,45],83:[2,45],84:[2,45],85:[2,45],87:[2,45]},{23:[2,44],33:[2,44],54:[2,44],65:[2,44],68:[2,44],72:[2,44],75:[2,44],80:[2,44],81:[2,44],82:[2,44],83:[2,44],84:[2,44],85:[2,44],87:[2,44]},{54:[1,109]},{54:[2,83],65:[2,83],72:[2,83],80:[2,83],81:[2,83],82:[2,83],83:[2,83],84:[2,83],85:[2,83]},{54:[2,85]},{5:[2,13],14:[2,13],15:[2,13],19:[2,13],29:[2,13],34:[2,13],39:[2,13],44:[2,13],47:[2,13],48:[2,13],51:[2,13],55:[2,13],60:[2,13]},{38:55,39:[1,57],43:56,44:[1,58],45:111,46:110,47:[2,76]},{33:[2,70],40:112,65:[2,70],72:[2,70],75:[2,70],80:[2,70],81:[2,70],82:[2,70],83:[2,70],84:[2,70],85:[2,70]},{47:[2,18]},{5:[2,14],14:[2,14],15:[2,14],19:[2,14],29:[2,14],34:[2,14],39:[2,14],44:[2,14],47:[2,14],48:[2,14],51:[2,14],55:[2,14],60:[2,14]},{33:[1,113]},{33:[2,87],65:[2,87],72:[2,87],80:[2,87],81:[2,87],82:[2,87],83:[2,87],84:[2,87],85:[2,87]},{33:[2,89]},{20:74,63:115,64:75,65:[1,43],67:114,68:[2,96],69:116,70:76,71:77,72:[1,78],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{33:[1,117]},{32:118,33:[2,62],74:119,75:[1,120]},{33:[2,59],65:[2,59],72:[2,59],75:[2,59],80:[2,59],81:[2,59],82:[2,59],83:[2,59],84:[2,59],85:[2,59]},{33:[2,61],75:[2,61]},{33:[2,68],37:121,74:122,75:[1,120]},{33:[2,65],65:[2,65],72:[2,65],75:[2,65],80:[2,65],81:[2,65],82:[2,65],83:[2,65],84:[2,65],85:[2,65]},{33:[2,67],75:[2,67]},{23:[1,123]},{23:[2,51],65:[2,51],72:[2,51],80:[2,51],81:[2,51],82:[2,51],83:[2,51],84:[2,51],85:[2,51]},{23:[2,53]},{33:[1,124]},{33:[2,91],65:[2,91],72:[2,91],80:[2,91],81:[2,91],82:[2,91],83:[2,91],84:[2,91],85:[2,91]},{33:[2,93]},{5:[2,22],14:[2,22],15:[2,22],19:[2,22],29:[2,22],34:[2,22],39:[2,22],44:[2,22],47:[2,22],48:[2,22],51:[2,22],55:[2,22],60:[2,22]},{23:[2,99],33:[2,99],54:[2,99],68:[2,99],72:[2,99],75:[2,99]},{73:[1,108]},{20:74,63:125,64:75,65:[1,43],72:[1,35],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{5:[2,23],14:[2,23],15:[2,23],19:[2,23],29:[2,23],34:[2,23],39:[2,23],44:[2,23],47:[2,23],48:[2,23],51:[2,23],55:[2,23],60:[2,23]},{47:[2,19]},{47:[2,77]},{20:74,33:[2,72],41:126,63:127,64:75,65:[1,43],69:128,70:76,71:77,72:[1,78],75:[2,72],78:26,79:27,80:[1,28],81:[1,29],82:[1,30],83:[1,31],84:[1,32],85:[1,34],86:33},{5:[2,24],14:[2,24],15:[2,24],19:[2,24],29:[2,24],34:[2,24],39:[2,24],44:[2,24],47:[2,24],48:[2,24],51:[2,24],55:[2,24],60:[2,24]},{68:[1,129]},{65:[2,95],68:[2,95],72:[2,95],80:[2,95],81:[2,95],82:[2,95],83:[2,95],84:[2,95],85:[2,95]},{68:[2,97]},{5:[2,21],14:[2,21],15:[2,21],19:[2,21],29:[2,21],34:[2,21],39:[2,21],44:[2,21],47:[2,21],48:[2,21],51:[2,21],55:[2,21],60:[2,21]},{33:[1,130]},{33:[2,63]},{72:[1,132],76:131},{33:[1,133]},{33:[2,69]},{15:[2,12],18:[2,12]},{14:[2,26],15:[2,26],19:[2,26],29:[2,26],34:[2,26],47:[2,26],48:[2,26],51:[2,26],55:[2,26],60:[2,26]},{23:[2,31],33:[2,31],54:[2,31],68:[2,31],72:[2,31],75:[2,31]},{33:[2,74],42:134,74:135,75:[1,120]},{33:[2,71],65:[2,71],72:[2,71],75:[2,71],80:[2,71],81:[2,71],82:[2,71],83:[2,71],84:[2,71],85:[2,71]},{33:[2,73],75:[2,73]},{23:[2,29],33:[2,29],54:[2,29],65:[2,29],68:[2,29],72:[2,29],75:[2,29],80:[2,29],81:[2,29],82:[2,29],83:[2,29],84:[2,29],85:[2,29]},{14:[2,15],15:[2,15],19:[2,15],29:[2,15],34:[2,15],39:[2,15],44:[2,15],47:[2,15],48:[2,15],51:[2,15],55:[2,15],60:[2,15]},{72:[1,137],77:[1,136]},{72:[2,100],77:[2,100]},{14:[2,16],15:[2,16],19:[2,16],29:[2,16],34:[2,16],44:[2,16],47:[2,16],48:[2,16],51:[2,16],55:[2,16],60:[2,16]},{33:[1,138]},{33:[2,75]},{33:[2,32]},{72:[2,101],77:[2,101]},{14:[2,17],15:[2,17],19:[2,17],29:[2,17],34:[2,17],39:[2,17],44:[2,17],47:[2,17],48:[2,17],51:[2,17],55:[2,17],60:[2,17]}],defaultActions:{4:[2,1],54:[2,55],56:[2,20],60:[2,57],73:[2,81],82:[2,85],86:[2,18],90:[2,89],101:[2,53],104:[2,93],110:[2,19],111:[2,77],116:[2,97],119:[2,63],122:[2,69],135:[2,75],136:[2,32]},parseError:function(a,b){throw new Error(a)},parse:function(a){function b(){var a;return a=c.lexer.lex()||1,"number"!=typeof a&&(a=c.symbols_[a]||a),a}var c=this,d=[0],e=[null],f=[],g=this.table,h="",i=0,j=0,k=0;this.lexer.setInput(a),this.lexer.yy=this.yy,this.yy.lexer=this.lexer,this.yy.parser=this,"undefined"==typeof this.lexer.yylloc&&(this.lexer.yylloc={});var l=this.lexer.yylloc;f.push(l);var m=this.lexer.options&&this.lexer.options.ranges;"function"==typeof this.yy.parseError&&(this.parseError=this.yy.parseError);for(var n,o,p,q,r,s,t,u,v,w={};;){if(p=d[d.length-1],this.defaultActions[p]?q=this.defaultActions[p]:(null!==n&&"undefined"!=typeof n||(n=b()),q=g[p]&&g[p][n]),"undefined"==typeof q||!q.length||!q[0]){var x="";if(!k){v=[];for(s in g[p])this.terminals_[s]&&s>2&&v.push("'"+this.terminals_[s]+"'");x=this.lexer.showPosition?"Parse error on line "+(i+1)+":\n"+this.lexer.showPosition()+"\nExpecting "+v.join(", ")+", got '"+(this.terminals_[n]||n)+"'":"Parse error on line "+(i+1)+": Unexpected "+(1==n?"end of input":"'"+(this.terminals_[n]||n)+"'"),this.parseError(x,{text:this.lexer.match,token:this.terminals_[n]||n,line:this.lexer.yylineno,loc:l,expected:v})}}if(q[0]instanceof Array&&q.length>1)throw new Error("Parse Error: multiple actions possible at state: "+p+", token: "+n);switch(q[0]){case 1:d.push(n),e.push(this.lexer.yytext),f.push(this.lexer.yylloc),d.push(q[1]),n=null,o?(n=o,o=null):(j=this.lexer.yyleng,h=this.lexer.yytext,i=this.lexer.yylineno,l=this.lexer.yylloc,k>0&&k--);break;case 2:if(t=this.productions_[q[1]][1],w.$=e[e.length-t],w._$={first_line:f[f.length-(t||1)].first_line,last_line:f[f.length-1].last_line,first_column:f[f.length-(t||1)].first_column,last_column:f[f.length-1].last_column},m&&(w._$.range=[f[f.length-(t||1)].range[0],f[f.length-1].range[1]]),r=this.performAction.call(w,h,j,i,this.yy,q[1],e,f),"undefined"!=typeof r)return r;t&&(d=d.slice(0,-1*t*2),e=e.slice(0,-1*t),f=f.slice(0,-1*t)),d.push(this.productions_[q[1]][0]),e.push(w.$),f.push(w._$),u=g[d[d.length-2]][d[d.length-1]],d.push(u);break;case 3:return!0}}return!0}},c=function(){var a={EOF:1,parseError:function(a,b){if(!this.yy.parser)throw new Error(a);this.yy.parser.parseError(a,b)},setInput:function(a){return this._input=a,this._more=this._less=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},input:function(){var a=this._input[0];this.yytext+=a,this.yyleng++,this.offset++,this.match+=a,this.matched+=a;var b=a.match(/(?:\r\n?|\n).*/g);return b?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),a},unput:function(a){var b=a.length,c=a.split(/(?:\r\n?|\n)/g);this._input=a+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-b-1),this.offset-=b;var d=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),c.length-1&&(this.yylineno-=c.length-1);var e=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:c?(c.length===d.length?this.yylloc.first_column:0)+d[d.length-c.length].length-c[0].length:this.yylloc.first_column-b},this.options.ranges&&(this.yylloc.range=[e[0],e[0]+this.yyleng-b]),this},more:function(){return this._more=!0,this},less:function(a){this.unput(this.match.slice(a))},pastInput:function(){var a=this.matched.substr(0,this.matched.length-this.match.length);return(a.length>20?"...":"")+a.substr(-20).replace(/\n/g,"")},upcomingInput:function(){var a=this.match;return a.length<20&&(a+=this._input.substr(0,20-a.length)),(a.substr(0,20)+(a.length>20?"...":"")).replace(/\n/g,"")},showPosition:function(){var a=this.pastInput(),b=new Array(a.length+1).join("-");return a+this.upcomingInput()+"\n"+b+"^"},next:function(){if(this.done)return this.EOF;this._input||(this.done=!0);var a,b,c,d,e;this._more||(this.yytext="",this.match="");for(var f=this._currentRules(),g=0;g<f.length&&(c=this._input.match(this.rules[f[g]]),!c||b&&!(c[0].length>b[0].length)||(b=c,d=g,this.options.flex));g++);return b?(e=b[0].match(/(?:\r\n?|\n).*/g),e&&(this.yylineno+=e.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:e?e[e.length-1].length-e[e.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+b[0].length},this.yytext+=b[0],this.match+=b[0],this.matches=b,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._input=this._input.slice(b[0].length),this.matched+=b[0],a=this.performAction.call(this,this.yy,this,f[d],this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),a?a:void 0):""===this._input?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+". Unrecognized text.\n"+this.showPosition(),{text:"",token:null,line:this.yylineno})},lex:function(){var a=this.next();return"undefined"!=typeof a?a:this.lex()},begin:function(a){this.conditionStack.push(a)},popState:function(){return this.conditionStack.pop()},_currentRules:function(){return this.conditions[this.conditionStack[this.conditionStack.length-1]].rules},topState:function(){return this.conditionStack[this.conditionStack.length-2]},pushState:function(a){this.begin(a)}};return a.options={},a.performAction=function(a,b,c,d){function e(a,c){return b.yytext=b.yytext.substring(a,b.yyleng-c+a)}switch(c){case 0:if("\\\\"===b.yytext.slice(-2)?(e(0,1),this.begin("mu")):"\\"===b.yytext.slice(-1)?(e(0,1),this.begin("emu")):this.begin("mu"),b.yytext)return 15;break;case 1:return 15;case 2:return this.popState(),15;case 3:return this.begin("raw"),15;case 4:return this.popState(),"raw"===this.conditionStack[this.conditionStack.length-1]?15:(e(5,9),"END_RAW_BLOCK");case 5:return 15;case 6:return this.popState(),14;case 7:return 65;case 8:return 68;case 9:return 19;case 10:return this.popState(),this.begin("raw"),23;case 11:return 55;case 12:return 60;case 13:return 29;case 14:return 47;case 15:return this.popState(),44;case 16:return this.popState(),44;case 17:return 34;case 18:return 39;case 19:return 51;case 20:return 48;case 21:this.unput(b.yytext),this.popState(),this.begin("com");break;case 22:return this.popState(),14;case 23:return 48;case 24:return 73;case 25:return 72;case 26:return 72;case 27:return 87;case 28:break;case 29:return this.popState(),54;case 30:return this.popState(),33;case 31:return b.yytext=e(1,2).replace(/\\"/g,'"'),80;case 32:return b.yytext=e(1,2).replace(/\\'/g,"'"),80;case 33:return 85;case 34:return 82;case 35:return 82;case 36:return 83;case 37:return 84;case 38:return 81;case 39:return 75;case 40:return 77;case 41:return 72;case 42:return b.yytext=b.yytext.replace(/\\([\\\]])/g,"$1"),72;case 43:return"INVALID";case 44:return 5}},a.rules=[/^(?:[^\x00]*?(?=(\{\{)))/,/^(?:[^\x00]+)/,/^(?:[^\x00]{2,}?(?=(\{\{|\\\{\{|\\\\\{\{|$)))/,/^(?:\{\{\{\{(?=[^\/]))/,/^(?:\{\{\{\{\/[^\s!"#%-,\.\/;->@\[-\^`\{-~]+(?=[=}\s\/.])\}\}\}\})/,/^(?:[^\x00]+?(?=(\{\{\{\{)))/,/^(?:[\s\S]*?--(~)?\}\})/,/^(?:\()/,/^(?:\))/,/^(?:\{\{\{\{)/,/^(?:\}\}\}\})/,/^(?:\{\{(~)?>)/,/^(?:\{\{(~)?#>)/,/^(?:\{\{(~)?#\*?)/,/^(?:\{\{(~)?\/)/,/^(?:\{\{(~)?\^\s*(~)?\}\})/,/^(?:\{\{(~)?\s*else\s*(~)?\}\})/,/^(?:\{\{(~)?\^)/,/^(?:\{\{(~)?\s*else\b)/,/^(?:\{\{(~)?\{)/,/^(?:\{\{(~)?&)/,/^(?:\{\{(~)?!--)/,/^(?:\{\{(~)?![\s\S]*?\}\})/,/^(?:\{\{(~)?\*?)/,/^(?:=)/,/^(?:\.\.)/,/^(?:\.(?=([=~}\s\/.)|])))/,/^(?:[\/.])/,/^(?:\s+)/,/^(?:\}(~)?\}\})/,/^(?:(~)?\}\})/,/^(?:"(\\["]|[^"])*")/,/^(?:'(\\[']|[^'])*')/,/^(?:@)/,/^(?:true(?=([~}\s)])))/,/^(?:false(?=([~}\s)])))/,/^(?:undefined(?=([~}\s)])))/,/^(?:null(?=([~}\s)])))/,/^(?:-?[0-9]+(?:\.[0-9]+)?(?=([~}\s)])))/,/^(?:as\s+\|)/,/^(?:\|)/,/^(?:([^\s!"#%-,\.\/;->@\[-\^`\{-~]+(?=([=~}\s\/.)|]))))/,/^(?:\[(\\\]|[^\]])*\])/,/^(?:.)/,/^(?:$)/],a.conditions={mu:{rules:[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44],inclusive:!1},emu:{rules:[2],inclusive:!1},com:{rules:[6],inclusive:!1},raw:{rules:[3,4,5],inclusive:!1},INITIAL:{rules:[0,1,44],inclusive:!0}},a}();return b.lexer=c,a.prototype=b,b.Parser=a,new a}();b["default"]=c,a.exports=b["default"]},function(a,b,c){"use strict";function d(){var a=arguments.length<=0||void 0===arguments[0]?{}:arguments[0];this.options=a}function e(a,b,c){void 0===b&&(b=a.length);var d=a[b-1],e=a[b-2];return d?"ContentStatement"===d.type?(e||!c?/\r?\n\s*?$/:/(^|\r?\n)\s*?$/).test(d.original):void 0:c}function f(a,b,c){void 0===b&&(b=-1);var d=a[b+1],e=a[b+2];return d?"ContentStatement"===d.type?(e||!c?/^\s*?\r?\n/:/^\s*?(\r?\n|$)/).test(d.original):void 0:c}function g(a,b,c){var d=a[null==b?0:b+1];if(d&&"ContentStatement"===d.type&&(c||!d.rightStripped)){var e=d.value;d.value=d.value.replace(c?/^\s+/:/^[ \t]*\r?\n?/,""),d.rightStripped=d.value!==e}}function h(a,b,c){var d=a[null==b?a.length-1:b-1];if(d&&"ContentStatement"===d.type&&(c||!d.leftStripped)){var e=d.value;return d.value=d.value.replace(c?/\s+$/:/[ \t]+$/,""),d.leftStripped=d.value!==e,d.leftStripped}}var i=c(1)["default"];b.__esModule=!0;var j=c(49),k=i(j);d.prototype=new k["default"],d.prototype.Program=function(a){var b=!this.options.ignoreStandalone,c=!this.isRootSeen;this.isRootSeen=!0;for(var d=a.body,i=0,j=d.length;i<j;i++){var k=d[i],l=this.accept(k);if(l){var m=e(d,i,c),n=f(d,i,c),o=l.openStandalone&&m,p=l.closeStandalone&&n,q=l.inlineStandalone&&m&&n;l.close&&g(d,i,!0),l.open&&h(d,i,!0),b&&q&&(g(d,i),h(d,i)&&"PartialStatement"===k.type&&(k.indent=/([ \t]+$)/.exec(d[i-1].original)[1])),b&&o&&(g((k.program||k.inverse).body),h(d,i)),b&&p&&(g(d,i),h((k.inverse||k.program).body))}}return a},d.prototype.BlockStatement=d.prototype.DecoratorBlock=d.prototype.PartialBlockStatement=function(a){this.accept(a.program),this.accept(a.inverse);var b=a.program||a.inverse,c=a.program&&a.inverse,d=c,i=c;if(c&&c.chained)for(d=c.body[0].program;i.chained;)i=i.body[i.body.length-1].program;var j={open:a.openStrip.open,close:a.closeStrip.close,openStandalone:f(b.body),closeStandalone:e((d||b).body)};if(a.openStrip.close&&g(b.body,null,!0),c){var k=a.inverseStrip;k.open&&h(b.body,null,!0),k.close&&g(d.body,null,!0),a.closeStrip.open&&h(i.body,null,!0),!this.options.ignoreStandalone&&e(b.body)&&f(d.body)&&(h(b.body),g(d.body))}else a.closeStrip.open&&h(b.body,null,!0);return j},d.prototype.Decorator=d.prototype.MustacheStatement=function(a){return a.strip},d.prototype.PartialStatement=d.prototype.CommentStatement=function(a){var b=a.strip||{};return{inlineStandalone:!0,open:b.open,close:b.close}},b["default"]=d,a.exports=b["default"]},function(a,b,c){"use strict";function d(){this.parents=[]}function e(a){this.acceptRequired(a,"path"),this.acceptArray(a.params),this.acceptKey(a,"hash")}function f(a){e.call(this,a),this.acceptKey(a,"program"),this.acceptKey(a,"inverse")}function g(a){this.acceptRequired(a,"name"),this.acceptArray(a.params),this.acceptKey(a,"hash")}var h=c(1)["default"];b.__esModule=!0;var i=c(6),j=h(i);d.prototype={constructor:d,mutating:!1,acceptKey:function(a,b){var c=this.accept(a[b]);if(this.mutating){if(c&&!d.prototype[c.type])throw new j["default"]('Unexpected node type "'+c.type+'" found when accepting '+b+" on "+a.type);a[b]=c}},acceptRequired:function(a,b){if(this.acceptKey(a,b),!a[b])throw new j["default"](a.type+" requires "+b)},acceptArray:function(a){for(var b=0,c=a.length;b<c;b++)this.acceptKey(a,b),a[b]||(a.splice(b,1),b--,c--)},accept:function(a){if(a){if(!this[a.type])throw new j["default"]("Unknown type: "+a.type,a);this.current&&this.parents.unshift(this.current),this.current=a;var b=this[a.type](a);return this.current=this.parents.shift(),!this.mutating||b?b:b!==!1?a:void 0}},Program:function(a){this.acceptArray(a.body)},MustacheStatement:e,Decorator:e,BlockStatement:f,DecoratorBlock:f,PartialStatement:g,PartialBlockStatement:function(a){g.call(this,a),this.acceptKey(a,"program")},ContentStatement:function(){},CommentStatement:function(){},SubExpression:e,PathExpression:function(){},StringLiteral:function(){},NumberLiteral:function(){},BooleanLiteral:function(){},UndefinedLiteral:function(){},NullLiteral:function(){},Hash:function(a){this.acceptArray(a.pairs)},HashPair:function(a){this.acceptRequired(a,"value")}},b["default"]=d,a.exports=b["default"]},function(a,b,c){"use strict";function d(a,b){if(b=b.path?b.path.original:b,a.path.original!==b){var c={loc:a.path.loc};throw new q["default"](a.path.original+" doesn't match "+b,c)}}function e(a,b){this.source=a,this.start={line:b.first_line,column:b.first_column},this.end={line:b.last_line,column:b.last_column}}function f(a){return/^\[.*\]$/.test(a)?a.substring(1,a.length-1):a}function g(a,b){return{open:"~"===a.charAt(2),close:"~"===b.charAt(b.length-3)}}function h(a){return a.replace(/^\{\{~?!-?-?/,"").replace(/-?-?~?\}\}$/,"")}function i(a,b,c){c=this.locInfo(c);for(var d=a?"@":"",e=[],f=0,g=0,h=b.length;g<h;g++){var i=b[g].part,j=b[g].original!==i;if(d+=(b[g].separator||"")+i,j||".."!==i&&"."!==i&&"this"!==i)e.push(i);else{if(e.length>0)throw new q["default"]("Invalid path: "+d,{loc:c});".."===i&&f++}}return{type:"PathExpression",data:a,depth:f,parts:e,original:d,loc:c}}function j(a,b,c,d,e,f){var g=d.charAt(3)||d.charAt(2),h="{"!==g&&"&"!==g,i=/\*/.test(d);return{type:i?"Decorator":"MustacheStatement",path:a,params:b,hash:c,escaped:h,strip:e,loc:this.locInfo(f)}}function k(a,b,c,e){d(a,c),e=this.locInfo(e);var f={type:"Program",body:b,strip:{},loc:e};return{type:"BlockStatement",path:a.path,params:a.params,hash:a.hash,program:f,openStrip:{},inverseStrip:{},closeStrip:{},loc:e}}function l(a,b,c,e,f,g){e&&e.path&&d(a,e);var h=/\*/.test(a.open);b.blockParams=a.blockParams;var i=void 0,j=void 0;if(c){if(h)throw new q["default"]("Unexpected inverse block on decorator",c);c.chain&&(c.program.body[0].closeStrip=e.strip),j=c.strip,i=c.program}return f&&(f=i,i=b,b=f),{type:h?"DecoratorBlock":"BlockStatement",path:a.path,params:a.params,hash:a.hash,program:b,inverse:i,openStrip:a.strip,inverseStrip:j,closeStrip:e&&e.strip,loc:this.locInfo(g)}}function m(a,b){if(!b&&a.length){var c=a[0].loc,d=a[a.length-1].loc;c&&d&&(b={source:c.source,start:{line:c.start.line,column:c.start.column},end:{line:d.end.line,column:d.end.column}})}return{type:"Program",body:a,strip:{},loc:b}}function n(a,b,c,e){return d(a,c),{type:"PartialBlockStatement",name:a.path,params:a.params,hash:a.hash,program:b,openStrip:a.strip,closeStrip:c&&c.strip,loc:this.locInfo(e)}}var o=c(1)["default"];b.__esModule=!0,b.SourceLocation=e,b.id=f,b.stripFlags=g,b.stripComment=h,b.preparePath=i,b.prepareMustache=j,b.prepareRawBlock=k,b.prepareBlock=l,b.prepareProgram=m,b.preparePartialBlock=n;var p=c(6),q=o(p)},function(a,b,c){"use strict";function d(){}function e(a,b,c){if(null==a||"string"!=typeof a&&"Program"!==a.type)throw new l["default"]("You must pass a string or Handlebars AST to Handlebars.precompile. You passed "+a);b=b||{},"data"in b||(b.data=!0),b.compat&&(b.useDepths=!0);var d=c.parse(a,b),e=(new c.Compiler).compile(d,b);return(new c.JavaScriptCompiler).compile(e,b)}function f(a,b,c){function d(){var d=c.parse(a,b),e=(new c.Compiler).compile(d,b),f=(new c.JavaScriptCompiler).compile(e,b,void 0,!0);return c.template(f)}function e(a,b){return f||(f=d()),f.call(this,a,b)}if(void 0===b&&(b={}),null==a||"string"!=typeof a&&"Program"!==a.type)throw new l["default"]("You must pass a string or Handlebars AST to Handlebars.compile. You passed "+a);b=m.extend({},b),"data"in b||(b.data=!0),b.compat&&(b.useDepths=!0);var f=void 0;return e._setup=function(a){return f||(f=d()),f._setup(a)},e._child=function(a,b,c,e){return f||(f=d()),f._child(a,b,c,e)},e}function g(a,b){if(a===b)return!0;if(m.isArray(a)&&m.isArray(b)&&a.length===b.length){for(var c=0;c<a.length;c++)if(!g(a[c],b[c]))return!1;return!0}}function h(a){if(!a.path.parts){var b=a.path;a.path={type:"PathExpression",data:!1,depth:0,parts:[b.original+""],original:b.original+"",loc:b.loc}}}var i=c(34)["default"],j=c(1)["default"];b.__esModule=!0,b.Compiler=d,b.precompile=e,b.compile=f;var k=c(6),l=j(k),m=c(5),n=c(45),o=j(n),p=[].slice;d.prototype={compiler:d,equals:function(a){var b=this.opcodes.length;if(a.opcodes.length!==b)return!1;for(var c=0;c<b;c++){var d=this.opcodes[c],e=a.opcodes[c];if(d.opcode!==e.opcode||!g(d.args,e.args))return!1}b=this.children.length;for(var c=0;c<b;c++)if(!this.children[c].equals(a.children[c]))return!1;return!0},guid:0,compile:function(a,b){return this.sourceNode=[],this.opcodes=[],this.children=[],this.options=b,this.stringParams=b.stringParams,this.trackIds=b.trackIds,b.blockParams=b.blockParams||[],b.knownHelpers=m.extend(i(null),{helperMissing:!0,blockHelperMissing:!0,each:!0,"if":!0,unless:!0,"with":!0,log:!0,lookup:!0},b.knownHelpers),this.accept(a)},compileProgram:function(a){var b=new this.compiler,c=b.compile(a,this.options),d=this.guid++;return this.usePartial=this.usePartial||c.usePartial,this.children[d]=c,this.useDepths=this.useDepths||c.useDepths,d},accept:function(a){if(!this[a.type])throw new l["default"]("Unknown type: "+a.type,a);this.sourceNode.unshift(a);var b=this[a.type](a);return this.sourceNode.shift(),b},Program:function(a){this.options.blockParams.unshift(a.blockParams);for(var b=a.body,c=b.length,d=0;d<c;d++)this.accept(b[d]);return this.options.blockParams.shift(),this.isSimple=1===c,this.blockParams=a.blockParams?a.blockParams.length:0,this},BlockStatement:function(a){h(a);var b=a.program,c=a.inverse;b=b&&this.compileProgram(b),c=c&&this.compileProgram(c);var d=this.classifySexpr(a);"helper"===d?this.helperSexpr(a,b,c):"simple"===d?(this.simpleSexpr(a),this.opcode("pushProgram",b),this.opcode("pushProgram",c),this.opcode("emptyHash"),this.opcode("blockValue",a.path.original)):(this.ambiguousSexpr(a,b,c),this.opcode("pushProgram",b),this.opcode("pushProgram",c),this.opcode("emptyHash"),this.opcode("ambiguousBlockValue")),this.opcode("append")},DecoratorBlock:function(a){var b=a.program&&this.compileProgram(a.program),c=this.setupFullMustacheParams(a,b,void 0),d=a.path;this.useDecorators=!0,this.opcode("registerDecorator",c.length,d.original)},PartialStatement:function(a){this.usePartial=!0;var b=a.program;b&&(b=this.compileProgram(a.program));var c=a.params;if(c.length>1)throw new l["default"]("Unsupported number of partial arguments: "+c.length,a);c.length||(this.options.explicitPartialContext?this.opcode("pushLiteral","undefined"):c.push({type:"PathExpression",parts:[],depth:0}));var d=a.name.original,e="SubExpression"===a.name.type;e&&this.accept(a.name),this.setupFullMustacheParams(a,b,void 0,!0);var f=a.indent||"";this.options.preventIndent&&f&&(this.opcode("appendContent",f),f=""),this.opcode("invokePartial",e,d,f),this.opcode("append")},PartialBlockStatement:function(a){this.PartialStatement(a)},MustacheStatement:function(a){this.SubExpression(a),a.escaped&&!this.options.noEscape?this.opcode("appendEscaped"):this.opcode("append")},Decorator:function(a){this.DecoratorBlock(a)},ContentStatement:function(a){a.value&&this.opcode("appendContent",a.value)},CommentStatement:function(){},SubExpression:function(a){h(a);var b=this.classifySexpr(a);"simple"===b?this.simpleSexpr(a):"helper"===b?this.helperSexpr(a):this.ambiguousSexpr(a)},ambiguousSexpr:function(a,b,c){var d=a.path,e=d.parts[0],f=null!=b||null!=c;this.opcode("getContext",d.depth),this.opcode("pushProgram",b),this.opcode("pushProgram",c),d.strict=!0,this.accept(d),this.opcode("invokeAmbiguous",e,f)},simpleSexpr:function(a){var b=a.path;b.strict=!0,this.accept(b),this.opcode("resolvePossibleLambda")},helperSexpr:function(a,b,c){var d=this.setupFullMustacheParams(a,b,c),e=a.path,f=e.parts[0];if(this.options.knownHelpers[f])this.opcode("invokeKnownHelper",d.length,f);else{if(this.options.knownHelpersOnly)throw new l["default"]("You specified knownHelpersOnly, but used the unknown helper "+f,a);e.strict=!0,e.falsy=!0,this.accept(e),this.opcode("invokeHelper",d.length,e.original,o["default"].helpers.simpleId(e))}},PathExpression:function(a){this.addDepth(a.depth),this.opcode("getContext",a.depth);var b=a.parts[0],c=o["default"].helpers.scopedId(a),d=!a.depth&&!c&&this.blockParamIndex(b);d?this.opcode("lookupBlockParam",d,a.parts):b?a.data?(this.options.data=!0,this.opcode("lookupData",a.depth,a.parts,a.strict)):this.opcode("lookupOnContext",a.parts,a.falsy,a.strict,c):this.opcode("pushContext")},StringLiteral:function(a){this.opcode("pushString",a.value)},NumberLiteral:function(a){this.opcode("pushLiteral",a.value)},BooleanLiteral:function(a){this.opcode("pushLiteral",a.value)},UndefinedLiteral:function(){this.opcode("pushLiteral","undefined")},NullLiteral:function(){this.opcode("pushLiteral","null")},Hash:function(a){var b=a.pairs,c=0,d=b.length;for(this.opcode("pushHash");c<d;c++)this.pushParam(b[c].value);for(;c--;)this.opcode("assignToHash",b[c].key);this.opcode("popHash")},opcode:function(a){this.opcodes.push({opcode:a,args:p.call(arguments,1),loc:this.sourceNode[0].loc})},addDepth:function(a){a&&(this.useDepths=!0)},classifySexpr:function(a){var b=o["default"].helpers.simpleId(a.path),c=b&&!!this.blockParamIndex(a.path.parts[0]),d=!c&&o["default"].helpers.helperExpression(a),e=!c&&(d||b);if(e&&!d){var f=a.path.parts[0],g=this.options;g.knownHelpers[f]?d=!0:g.knownHelpersOnly&&(e=!1)}return d?"helper":e?"ambiguous":"simple"},pushParams:function(a){for(var b=0,c=a.length;b<c;b++)this.pushParam(a[b])},pushParam:function(a){var b=null!=a.value?a.value:a.original||"";if(this.stringParams)b.replace&&(b=b.replace(/^(\.?\.\/)*/g,"").replace(/\//g,".")),a.depth&&this.addDepth(a.depth),this.opcode("getContext",a.depth||0),this.opcode("pushStringParam",b,a.type),"SubExpression"===a.type&&this.accept(a);else{if(this.trackIds){var c=void 0;if(!a.parts||o["default"].helpers.scopedId(a)||a.depth||(c=this.blockParamIndex(a.parts[0])),c){var d=a.parts.slice(1).join(".");this.opcode("pushId","BlockParam",c,d)}else b=a.original||b,b.replace&&(b=b.replace(/^this(?:\.|$)/,"").replace(/^\.\//,"").replace(/^\.$/,"")),this.opcode("pushId",a.type,b)}this.accept(a)}},setupFullMustacheParams:function(a,b,c,d){var e=a.params;return this.pushParams(e),this.opcode("pushProgram",b),this.opcode("pushProgram",c),a.hash?this.accept(a.hash):this.opcode("emptyHash",d),e},blockParamIndex:function(a){for(var b=0,c=this.options.blockParams.length;b<c;b++){var d=this.options.blockParams[b],e=d&&m.indexOf(d,a);if(d&&e>=0)return[b,e]}}}},function(a,b,c){"use strict";function d(a){this.value=a}function e(){}function f(a,b,c,d){var e=b.popStack(),f=0,g=c.length;for(a&&g--;f<g;f++)e=b.nameLookup(e,c[f],d);return a?[b.aliasable("container.strict"),"(",e,", ",b.quotedString(c[f]),", ",JSON.stringify(b.source.currentLocation)," )"]:e}var g=c(13)["default"],h=c(1)["default"];b.__esModule=!0;var i=c(4),j=c(6),k=h(j),l=c(5),m=c(53),n=h(m);e.prototype={nameLookup:function(a,b){return this.internalNameLookup(a,b)},depthedLookup:function(a){return[this.aliasable("container.lookup"),"(depths, ",JSON.stringify(a),")"]},compilerInfo:function(){var a=i.COMPILER_REVISION,b=i.REVISION_CHANGES[a];return[a,b]},appendToBuffer:function(a,b,c){return l.isArray(a)||(a=[a]),a=this.source.wrap(a,b),this.environment.isSimple?["return ",a,";"]:c?["buffer += ",a,";"]:(a.appendToBuffer=!0,a)},initializeBuffer:function(){return this.quotedString("")},internalNameLookup:function(a,b){return this.lookupPropertyFunctionIsUsed=!0,["lookupProperty(",a,",",JSON.stringify(b),")"]},lookupPropertyFunctionIsUsed:!1,compile:function(a,b,c,d){this.environment=a,this.options=b,this.stringParams=this.options.stringParams,this.trackIds=this.options.trackIds,this.precompile=!d,this.name=this.environment.name,this.isChild=!!c,this.context=c||{decorators:[],programs:[],environments:[]},this.preamble(),this.stackSlot=0,this.stackVars=[],this.aliases={},this.registers={list:[]},this.hashes=[],this.compileStack=[],this.inlineStack=[],this.blockParams=[],this.compileChildren(a,b),this.useDepths=this.useDepths||a.useDepths||a.useDecorators||this.options.compat,this.useBlockParams=this.useBlockParams||a.useBlockParams;var e=a.opcodes,f=void 0,g=void 0,h=void 0,i=void 0;for(h=0,i=e.length;h<i;h++)f=e[h],this.source.currentLocation=f.loc,g=g||f.loc,this[f.opcode].apply(this,f.args);if(this.source.currentLocation=g,this.pushSource(""),this.stackSlot||this.inlineStack.length||this.compileStack.length)throw new k["default"]("Compile completed with content left on stack");this.decorators.isEmpty()?this.decorators=void 0:(this.useDecorators=!0,this.decorators.prepend(["var decorators = container.decorators, ",this.lookupPropertyFunctionVarDeclaration(),";\n"]),
        this.decorators.push("return fn;"),d?this.decorators=Function.apply(this,["fn","props","container","depth0","data","blockParams","depths",this.decorators.merge()]):(this.decorators.prepend("function(fn, props, container, depth0, data, blockParams, depths) {\n"),this.decorators.push("}\n"),this.decorators=this.decorators.merge()));var j=this.createFunctionContext(d);if(this.isChild)return j;var l={compiler:this.compilerInfo(),main:j};this.decorators&&(l.main_d=this.decorators,l.useDecorators=!0);var m=this.context,n=m.programs,o=m.decorators;for(h=0,i=n.length;h<i;h++)n[h]&&(l[h]=n[h],o[h]&&(l[h+"_d"]=o[h],l.useDecorators=!0));return this.environment.usePartial&&(l.usePartial=!0),this.options.data&&(l.useData=!0),this.useDepths&&(l.useDepths=!0),this.useBlockParams&&(l.useBlockParams=!0),this.options.compat&&(l.compat=!0),d?l.compilerOptions=this.options:(l.compiler=JSON.stringify(l.compiler),this.source.currentLocation={start:{line:1,column:0}},l=this.objectLiteral(l),b.srcName?(l=l.toStringWithSourceMap({file:b.destName}),l.map=l.map&&l.map.toString()):l=l.toString()),l},preamble:function(){this.lastContext=0,this.source=new n["default"](this.options.srcName),this.decorators=new n["default"](this.options.srcName)},createFunctionContext:function(a){var b=this,c="",d=this.stackVars.concat(this.registers.list);d.length>0&&(c+=", "+d.join(", "));var e=0;g(this.aliases).forEach(function(a){var d=b.aliases[a];d.children&&d.referenceCount>1&&(c+=", alias"+ ++e+"="+a,d.children[0]="alias"+e)}),this.lookupPropertyFunctionIsUsed&&(c+=", "+this.lookupPropertyFunctionVarDeclaration());var f=["container","depth0","helpers","partials","data"];(this.useBlockParams||this.useDepths)&&f.push("blockParams"),this.useDepths&&f.push("depths");var h=this.mergeSource(c);return a?(f.push(h),Function.apply(this,f)):this.source.wrap(["function(",f.join(","),") {\n  ",h,"}"])},mergeSource:function(a){var b=this.environment.isSimple,c=!this.forceBuffer,d=void 0,e=void 0,f=void 0,g=void 0;return this.source.each(function(a){a.appendToBuffer?(f?a.prepend("  + "):f=a,g=a):(f&&(e?f.prepend("buffer += "):d=!0,g.add(";"),f=g=void 0),e=!0,b||(c=!1))}),c?f?(f.prepend("return "),g.add(";")):e||this.source.push('return "";'):(a+=", buffer = "+(d?"":this.initializeBuffer()),f?(f.prepend("return buffer + "),g.add(";")):this.source.push("return buffer;")),a&&this.source.prepend("var "+a.substring(2)+(d?"":";\n")),this.source.merge()},lookupPropertyFunctionVarDeclaration:function(){return"\n      lookupProperty = container.lookupProperty || function(parent, propertyName) {\n        if (Object.prototype.hasOwnProperty.call(parent, propertyName)) {\n          return parent[propertyName];\n        }\n        return undefined\n    }\n    ".trim()},blockValue:function(a){var b=this.aliasable("container.hooks.blockHelperMissing"),c=[this.contextName(0)];this.setupHelperArgs(a,0,c);var d=this.popStack();c.splice(1,0,d),this.push(this.source.functionCall(b,"call",c))},ambiguousBlockValue:function(){var a=this.aliasable("container.hooks.blockHelperMissing"),b=[this.contextName(0)];this.setupHelperArgs("",0,b,!0),this.flushInline();var c=this.topStack();b.splice(1,0,c),this.pushSource(["if (!",this.lastHelper,") { ",c," = ",this.source.functionCall(a,"call",b),"}"])},appendContent:function(a){this.pendingContent?a=this.pendingContent+a:this.pendingLocation=this.source.currentLocation,this.pendingContent=a},append:function(){if(this.isInline())this.replaceStack(function(a){return[" != null ? ",a,' : ""']}),this.pushSource(this.appendToBuffer(this.popStack()));else{var a=this.popStack();this.pushSource(["if (",a," != null) { ",this.appendToBuffer(a,void 0,!0)," }"]),this.environment.isSimple&&this.pushSource(["else { ",this.appendToBuffer("''",void 0,!0)," }"])}},appendEscaped:function(){this.pushSource(this.appendToBuffer([this.aliasable("container.escapeExpression"),"(",this.popStack(),")"]))},getContext:function(a){this.lastContext=a},pushContext:function(){this.pushStackLiteral(this.contextName(this.lastContext))},lookupOnContext:function(a,b,c,d){var e=0;d||!this.options.compat||this.lastContext?this.pushContext():this.push(this.depthedLookup(a[e++])),this.resolvePath("context",a,e,b,c)},lookupBlockParam:function(a,b){this.useBlockParams=!0,this.push(["blockParams[",a[0],"][",a[1],"]"]),this.resolvePath("context",b,1)},lookupData:function(a,b,c){a?this.pushStackLiteral("container.data(data, "+a+")"):this.pushStackLiteral("data"),this.resolvePath("data",b,0,!0,c)},resolvePath:function(a,b,c,d,e){var g=this;if(this.options.strict||this.options.assumeObjects)return void this.push(f(this.options.strict&&e,this,b,a));for(var h=b.length;c<h;c++)this.replaceStack(function(e){var f=g.nameLookup(e,b[c],a);return d?[" && ",f]:[" != null ? ",f," : ",e]})},resolvePossibleLambda:function(){this.push([this.aliasable("container.lambda"),"(",this.popStack(),", ",this.contextName(0),")"])},pushStringParam:function(a,b){this.pushContext(),this.pushString(b),"SubExpression"!==b&&("string"==typeof a?this.pushString(a):this.pushStackLiteral(a))},emptyHash:function(a){this.trackIds&&this.push("{}"),this.stringParams&&(this.push("{}"),this.push("{}")),this.pushStackLiteral(a?"undefined":"{}")},pushHash:function(){this.hash&&this.hashes.push(this.hash),this.hash={values:{},types:[],contexts:[],ids:[]}},popHash:function(){var a=this.hash;this.hash=this.hashes.pop(),this.trackIds&&this.push(this.objectLiteral(a.ids)),this.stringParams&&(this.push(this.objectLiteral(a.contexts)),this.push(this.objectLiteral(a.types))),this.push(this.objectLiteral(a.values))},pushString:function(a){this.pushStackLiteral(this.quotedString(a))},pushLiteral:function(a){this.pushStackLiteral(a)},pushProgram:function(a){null!=a?this.pushStackLiteral(this.programExpression(a)):this.pushStackLiteral(null)},registerDecorator:function(a,b){var c=this.nameLookup("decorators",b,"decorator"),d=this.setupHelperArgs(b,a);this.decorators.push(["fn = ",this.decorators.functionCall(c,"",["fn","props","container",d])," || fn;"])},invokeHelper:function(a,b,c){var d=this.popStack(),e=this.setupHelper(a,b),f=[];c&&f.push(e.name),f.push(d),this.options.strict||f.push(this.aliasable("container.hooks.helperMissing"));var g=["(",this.itemsSeparatedBy(f,"||"),")"],h=this.source.functionCall(g,"call",e.callParams);this.push(h)},itemsSeparatedBy:function(a,b){var c=[];c.push(a[0]);for(var d=1;d<a.length;d++)c.push(b,a[d]);return c},invokeKnownHelper:function(a,b){var c=this.setupHelper(a,b);this.push(this.source.functionCall(c.name,"call",c.callParams))},invokeAmbiguous:function(a,b){this.useRegister("helper");var c=this.popStack();this.emptyHash();var d=this.setupHelper(0,a,b),e=this.lastHelper=this.nameLookup("helpers",a,"helper"),f=["(","(helper = ",e," || ",c,")"];this.options.strict||(f[0]="(helper = ",f.push(" != null ? helper : ",this.aliasable("container.hooks.helperMissing"))),this.push(["(",f,d.paramsInit?["),(",d.paramsInit]:[],"),","(typeof helper === ",this.aliasable('"function"')," ? ",this.source.functionCall("helper","call",d.callParams)," : helper))"])},invokePartial:function(a,b,c){var d=[],e=this.setupParams(b,1,d);a&&(b=this.popStack(),delete e.name),c&&(e.indent=JSON.stringify(c)),e.helpers="helpers",e.partials="partials",e.decorators="container.decorators",a?d.unshift(b):d.unshift(this.nameLookup("partials",b,"partial")),this.options.compat&&(e.depths="depths"),e=this.objectLiteral(e),d.push(e),this.push(this.source.functionCall("container.invokePartial","",d))},assignToHash:function(a){var b=this.popStack(),c=void 0,d=void 0,e=void 0;this.trackIds&&(e=this.popStack()),this.stringParams&&(d=this.popStack(),c=this.popStack());var f=this.hash;c&&(f.contexts[a]=c),d&&(f.types[a]=d),e&&(f.ids[a]=e),f.values[a]=b},pushId:function(a,b,c){"BlockParam"===a?this.pushStackLiteral("blockParams["+b[0]+"].path["+b[1]+"]"+(c?" + "+JSON.stringify("."+c):"")):"PathExpression"===a?this.pushString(b):"SubExpression"===a?this.pushStackLiteral("true"):this.pushStackLiteral("null")},compiler:e,compileChildren:function(a,b){for(var c=a.children,d=void 0,e=void 0,f=0,g=c.length;f<g;f++){d=c[f],e=new this.compiler;var h=this.matchExistingProgram(d);if(null==h){this.context.programs.push("");var i=this.context.programs.length;d.index=i,d.name="program"+i,this.context.programs[i]=e.compile(d,b,this.context,!this.precompile),this.context.decorators[i]=e.decorators,this.context.environments[i]=d,this.useDepths=this.useDepths||e.useDepths,this.useBlockParams=this.useBlockParams||e.useBlockParams,d.useDepths=this.useDepths,d.useBlockParams=this.useBlockParams}else d.index=h.index,d.name="program"+h.index,this.useDepths=this.useDepths||h.useDepths,this.useBlockParams=this.useBlockParams||h.useBlockParams}},matchExistingProgram:function(a){for(var b=0,c=this.context.environments.length;b<c;b++){var d=this.context.environments[b];if(d&&d.equals(a))return d}},programExpression:function(a){var b=this.environment.children[a],c=[b.index,"data",b.blockParams];return(this.useBlockParams||this.useDepths)&&c.push("blockParams"),this.useDepths&&c.push("depths"),"container.program("+c.join(", ")+")"},useRegister:function(a){this.registers[a]||(this.registers[a]=!0,this.registers.list.push(a))},push:function(a){return a instanceof d||(a=this.source.wrap(a)),this.inlineStack.push(a),a},pushStackLiteral:function(a){this.push(new d(a))},pushSource:function(a){this.pendingContent&&(this.source.push(this.appendToBuffer(this.source.quotedString(this.pendingContent),this.pendingLocation)),this.pendingContent=void 0),a&&this.source.push(a)},replaceStack:function(a){var b=["("],c=void 0,e=void 0,f=void 0;if(!this.isInline())throw new k["default"]("replaceStack on non-inline");var g=this.popStack(!0);if(g instanceof d)c=[g.value],b=["(",c],f=!0;else{e=!0;var h=this.incrStack();b=["((",this.push(h)," = ",g,")"],c=this.topStack()}var i=a.call(this,c);f||this.popStack(),e&&this.stackSlot--,this.push(b.concat(i,")"))},incrStack:function(){return this.stackSlot++,this.stackSlot>this.stackVars.length&&this.stackVars.push("stack"+this.stackSlot),this.topStackName()},topStackName:function(){return"stack"+this.stackSlot},flushInline:function(){var a=this.inlineStack;this.inlineStack=[];for(var b=0,c=a.length;b<c;b++){var e=a[b];if(e instanceof d)this.compileStack.push(e);else{var f=this.incrStack();this.pushSource([f," = ",e,";"]),this.compileStack.push(f)}}},isInline:function(){return this.inlineStack.length},popStack:function(a){var b=this.isInline(),c=(b?this.inlineStack:this.compileStack).pop();if(!a&&c instanceof d)return c.value;if(!b){if(!this.stackSlot)throw new k["default"]("Invalid stack pop");this.stackSlot--}return c},topStack:function(){var a=this.isInline()?this.inlineStack:this.compileStack,b=a[a.length-1];return b instanceof d?b.value:b},contextName:function(a){return this.useDepths&&a?"depths["+a+"]":"depth"+a},quotedString:function(a){return this.source.quotedString(a)},objectLiteral:function(a){return this.source.objectLiteral(a)},aliasable:function(a){var b=this.aliases[a];return b?(b.referenceCount++,b):(b=this.aliases[a]=this.source.wrap(a),b.aliasable=!0,b.referenceCount=1,b)},setupHelper:function(a,b,c){var d=[],e=this.setupHelperArgs(b,a,d,c),f=this.nameLookup("helpers",b,"helper"),g=this.aliasable(this.contextName(0)+" != null ? "+this.contextName(0)+" : (container.nullContext || {})");return{params:d,paramsInit:e,name:f,callParams:[g].concat(d)}},setupParams:function(a,b,c){var d={},e=[],f=[],g=[],h=!c,i=void 0;h&&(c=[]),d.name=this.quotedString(a),d.hash=this.popStack(),this.trackIds&&(d.hashIds=this.popStack()),this.stringParams&&(d.hashTypes=this.popStack(),d.hashContexts=this.popStack());var j=this.popStack(),k=this.popStack();(k||j)&&(d.fn=k||"container.noop",d.inverse=j||"container.noop");for(var l=b;l--;)i=this.popStack(),c[l]=i,this.trackIds&&(g[l]=this.popStack()),this.stringParams&&(f[l]=this.popStack(),e[l]=this.popStack());return h&&(d.args=this.source.generateArray(c)),this.trackIds&&(d.ids=this.source.generateArray(g)),this.stringParams&&(d.types=this.source.generateArray(f),d.contexts=this.source.generateArray(e)),this.options.data&&(d.data="data"),this.useBlockParams&&(d.blockParams="blockParams"),d},setupHelperArgs:function(a,b,c,d){var e=this.setupParams(a,b,c);return e.loc=JSON.stringify(this.source.currentLocation),e=this.objectLiteral(e),d?(this.useRegister("options"),c.push("options"),["options=",e]):c?(c.push(e),""):e}},function(){for(var a="break else new var case finally return void catch for switch while continue function this with default if throw delete in try do instanceof typeof abstract enum int short boolean export interface static byte extends long super char final native synchronized class float package throws const goto private transient debugger implements protected volatile double import public let yield await null true false".split(" "),b=e.RESERVED_WORDS={},c=0,d=a.length;c<d;c++)b[a[c]]=!0}(),e.isValidJavaScriptVariableName=function(a){return!e.RESERVED_WORDS[a]&&/^[a-zA-Z_$][0-9a-zA-Z_$]*$/.test(a)},b["default"]=e,a.exports=b["default"]},function(a,b,c){"use strict";function d(a,b,c){if(g.isArray(a)){for(var d=[],e=0,f=a.length;e<f;e++)d.push(b.wrap(a[e],c));return d}return"boolean"==typeof a||"number"==typeof a?a+"":a}function e(a){this.srcFile=a,this.source=[]}var f=c(13)["default"];b.__esModule=!0;var g=c(5),h=void 0;try{}catch(i){}h||(h=function(a,b,c,d){this.src="",d&&this.add(d)},h.prototype={add:function(a){g.isArray(a)&&(a=a.join("")),this.src+=a},prepend:function(a){g.isArray(a)&&(a=a.join("")),this.src=a+this.src},toStringWithSourceMap:function(){return{code:this.toString()}},toString:function(){return this.src}}),e.prototype={isEmpty:function(){return!this.source.length},prepend:function(a,b){this.source.unshift(this.wrap(a,b))},push:function(a,b){this.source.push(this.wrap(a,b))},merge:function(){var a=this.empty();return this.each(function(b){a.add(["  ",b,"\n"])}),a},each:function(a){for(var b=0,c=this.source.length;b<c;b++)a(this.source[b])},empty:function(){var a=this.currentLocation||{start:{}};return new h(a.start.line,a.start.column,this.srcFile)},wrap:function(a){var b=arguments.length<=1||void 0===arguments[1]?this.currentLocation||{start:{}}:arguments[1];return a instanceof h?a:(a=d(a,this,b),new h(b.start.line,b.start.column,this.srcFile,a))},functionCall:function(a,b,c){return c=this.generateList(c),this.wrap([a,b?"."+b+"(":"(",c,")"])},quotedString:function(a){return'"'+(a+"").replace(/\\/g,"\\\\").replace(/"/g,'\\"').replace(/\n/g,"\\n").replace(/\r/g,"\\r").replace(/\u2028/g,"\\u2028").replace(/\u2029/g,"\\u2029")+'"'},objectLiteral:function(a){var b=this,c=[];f(a).forEach(function(e){var f=d(a[e],b);"undefined"!==f&&c.push([b.quotedString(e),":",f])});var e=this.generateList(c);return e.prepend("{"),e.add("}"),e},generateList:function(a){for(var b=this.empty(),c=0,e=a.length;c<e;c++)c&&b.add(","),b.add(d(a[c],this));return b},generateArray:function(a){var b=this.generateList(a);return b.prepend("["),b.add("]"),b}},b["default"]=e,a.exports=b["default"]}])});;
/*! lazysizes - v5.3.2 */

!function(e){var t=function(u,D,f){"use strict";var k,H;if(function(){var e;var t={lazyClass:"lazyload",loadedClass:"lazyloaded",loadingClass:"lazyloading",preloadClass:"lazypreload",errorClass:"lazyerror",autosizesClass:"lazyautosizes",fastLoadedClass:"ls-is-cached",iframeLoadMode:0,srcAttr:"data-src",srcsetAttr:"data-srcset",sizesAttr:"data-sizes",minSize:40,customMedia:{},init:true,expFactor:1.5,hFac:.8,loadMode:2,loadHidden:true,ricTimeout:0,throttleDelay:125};H=u.lazySizesConfig||u.lazysizesConfig||{};for(e in t){if(!(e in H)){H[e]=t[e]}}}(),!D||!D.getElementsByClassName){return{init:function(){},cfg:H,noSupport:true}}var O=D.documentElement,i=u.HTMLPictureElement,P="addEventListener",$="getAttribute",q=u[P].bind(u),I=u.setTimeout,U=u.requestAnimationFrame||I,o=u.requestIdleCallback,j=/^picture$/i,r=["load","error","lazyincluded","_lazyloaded"],a={},G=Array.prototype.forEach,J=function(e,t){if(!a[t]){a[t]=new RegExp("(\\s|^)"+t+"(\\s|$)")}return a[t].test(e[$]("class")||"")&&a[t]},K=function(e,t){if(!J(e,t)){e.setAttribute("class",(e[$]("class")||"").trim()+" "+t)}},Q=function(e,t){var a;if(a=J(e,t)){e.setAttribute("class",(e[$]("class")||"").replace(a," "))}},V=function(t,a,e){var i=e?P:"removeEventListener";if(e){V(t,a)}r.forEach(function(e){t[i](e,a)})},X=function(e,t,a,i,r){var n=D.createEvent("Event");if(!a){a={}}a.instance=k;n.initEvent(t,!i,!r);n.detail=a;e.dispatchEvent(n);return n},Y=function(e,t){var a;if(!i&&(a=u.picturefill||H.pf)){if(t&&t.src&&!e[$]("srcset")){e.setAttribute("srcset",t.src)}a({reevaluate:true,elements:[e]})}else if(t&&t.src){e.src=t.src}},Z=function(e,t){return(getComputedStyle(e,null)||{})[t]},s=function(e,t,a){a=a||e.offsetWidth;while(a<H.minSize&&t&&!e._lazysizesWidth){a=t.offsetWidth;t=t.parentNode}return a},ee=function(){var a,i;var t=[];var r=[];var n=t;var s=function(){var e=n;n=t.length?r:t;a=true;i=false;while(e.length){e.shift()()}a=false};var e=function(e,t){if(a&&!t){e.apply(this,arguments)}else{n.push(e);if(!i){i=true;(D.hidden?I:U)(s)}}};e._lsFlush=s;return e}(),te=function(a,e){return e?function(){ee(a)}:function(){var e=this;var t=arguments;ee(function(){a.apply(e,t)})}},ae=function(e){var a;var i=0;var r=H.throttleDelay;var n=H.ricTimeout;var t=function(){a=false;i=f.now();e()};var s=o&&n>49?function(){o(t,{timeout:n});if(n!==H.ricTimeout){n=H.ricTimeout}}:te(function(){I(t)},true);return function(e){var t;if(e=e===true){n=33}if(a){return}a=true;t=r-(f.now()-i);if(t<0){t=0}if(e||t<9){s()}else{I(s,t)}}},ie=function(e){var t,a;var i=99;var r=function(){t=null;e()};var n=function(){var e=f.now()-a;if(e<i){I(n,i-e)}else{(o||r)(r)}};return function(){a=f.now();if(!t){t=I(n,i)}}},e=function(){var v,m,c,h,e;var y,z,g,p,C,b,A;var n=/^img$/i;var d=/^iframe$/i;var E="onscroll"in u&&!/(gle|ing)bot/.test(navigator.userAgent);var _=0;var w=0;var M=0;var N=-1;var L=function(e){M--;if(!e||M<0||!e.target){M=0}};var x=function(e){if(A==null){A=Z(D.body,"visibility")=="hidden"}return A||!(Z(e.parentNode,"visibility")=="hidden"&&Z(e,"visibility")=="hidden")};var W=function(e,t){var a;var i=e;var r=x(e);g-=t;b+=t;p-=t;C+=t;while(r&&(i=i.offsetParent)&&i!=D.body&&i!=O){r=(Z(i,"opacity")||1)>0;if(r&&Z(i,"overflow")!="visible"){a=i.getBoundingClientRect();r=C>a.left&&p<a.right&&b>a.top-1&&g<a.bottom+1}}return r};var t=function(){var e,t,a,i,r,n,s,o,l,u,f,c;var d=k.elements;if((h=H.loadMode)&&M<8&&(e=d.length)){t=0;N++;for(;t<e;t++){if(!d[t]||d[t]._lazyRace){continue}if(!E||k.prematureUnveil&&k.prematureUnveil(d[t])){R(d[t]);continue}if(!(o=d[t][$]("data-expand"))||!(n=o*1)){n=w}if(!u){u=!H.expand||H.expand<1?O.clientHeight>500&&O.clientWidth>500?500:370:H.expand;k._defEx=u;f=u*H.expFactor;c=H.hFac;A=null;if(w<f&&M<1&&N>2&&h>2&&!D.hidden){w=f;N=0}else if(h>1&&N>1&&M<6){w=u}else{w=_}}if(l!==n){y=innerWidth+n*c;z=innerHeight+n;s=n*-1;l=n}a=d[t].getBoundingClientRect();if((b=a.bottom)>=s&&(g=a.top)<=z&&(C=a.right)>=s*c&&(p=a.left)<=y&&(b||C||p||g)&&(H.loadHidden||x(d[t]))&&(m&&M<3&&!o&&(h<3||N<4)||W(d[t],n))){R(d[t]);r=true;if(M>9){break}}else if(!r&&m&&!i&&M<4&&N<4&&h>2&&(v[0]||H.preloadAfterLoad)&&(v[0]||!o&&(b||C||p||g||d[t][$](H.sizesAttr)!="auto"))){i=v[0]||d[t]}}if(i&&!r){R(i)}}};var a=ae(t);var S=function(e){var t=e.target;if(t._lazyCache){delete t._lazyCache;return}L(e);K(t,H.loadedClass);Q(t,H.loadingClass);V(t,B);X(t,"lazyloaded")};var i=te(S);var B=function(e){i({target:e.target})};var T=function(e,t){var a=e.getAttribute("data-load-mode")||H.iframeLoadMode;if(a==0){e.contentWindow.location.replace(t)}else if(a==1){e.src=t}};var F=function(e){var t;var a=e[$](H.srcsetAttr);if(t=H.customMedia[e[$]("data-media")||e[$]("media")]){e.setAttribute("media",t)}if(a){e.setAttribute("srcset",a)}};var s=te(function(t,e,a,i,r){var n,s,o,l,u,f;if(!(u=X(t,"lazybeforeunveil",e)).defaultPrevented){if(i){if(a){K(t,H.autosizesClass)}else{t.setAttribute("sizes",i)}}s=t[$](H.srcsetAttr);n=t[$](H.srcAttr);if(r){o=t.parentNode;l=o&&j.test(o.nodeName||"")}f=e.firesLoad||"src"in t&&(s||n||l);u={target:t};K(t,H.loadingClass);if(f){clearTimeout(c);c=I(L,2500);V(t,B,true)}if(l){G.call(o.getElementsByTagName("source"),F)}if(s){t.setAttribute("srcset",s)}else if(n&&!l){if(d.test(t.nodeName)){T(t,n)}else{t.src=n}}if(r&&(s||l)){Y(t,{src:n})}}if(t._lazyRace){delete t._lazyRace}Q(t,H.lazyClass);ee(function(){var e=t.complete&&t.naturalWidth>1;if(!f||e){if(e){K(t,H.fastLoadedClass)}S(u);t._lazyCache=true;I(function(){if("_lazyCache"in t){delete t._lazyCache}},9)}if(t.loading=="lazy"){M--}},true)});var R=function(e){if(e._lazyRace){return}var t;var a=n.test(e.nodeName);var i=a&&(e[$](H.sizesAttr)||e[$]("sizes"));var r=i=="auto";if((r||!m)&&a&&(e[$]("src")||e.srcset)&&!e.complete&&!J(e,H.errorClass)&&J(e,H.lazyClass)){return}t=X(e,"lazyunveilread").detail;if(r){re.updateElem(e,true,e.offsetWidth)}e._lazyRace=true;M++;s(e,t,r,i,a)};var r=ie(function(){H.loadMode=3;a()});var o=function(){if(H.loadMode==3){H.loadMode=2}r()};var l=function(){if(m){return}if(f.now()-e<999){I(l,999);return}m=true;H.loadMode=3;a();q("scroll",o,true)};return{_:function(){e=f.now();k.elements=D.getElementsByClassName(H.lazyClass);v=D.getElementsByClassName(H.lazyClass+" "+H.preloadClass);q("scroll",a,true);q("resize",a,true);q("pageshow",function(e){if(e.persisted){var t=D.querySelectorAll("."+H.loadingClass);if(t.length&&t.forEach){U(function(){t.forEach(function(e){if(e.complete){R(e)}})})}}});if(u.MutationObserver){new MutationObserver(a).observe(O,{childList:true,subtree:true,attributes:true})}else{O[P]("DOMNodeInserted",a,true);O[P]("DOMAttrModified",a,true);setInterval(a,999)}q("hashchange",a,true);["focus","mouseover","click","load","transitionend","animationend"].forEach(function(e){D[P](e,a,true)});if(/d$|^c/.test(D.readyState)){l()}else{q("load",l);D[P]("DOMContentLoaded",a);I(l,2e4)}if(k.elements.length){t();ee._lsFlush()}else{a()}},checkElems:a,unveil:R,_aLSL:o}}(),re=function(){var a;var n=te(function(e,t,a,i){var r,n,s;e._lazysizesWidth=i;i+="px";e.setAttribute("sizes",i);if(j.test(t.nodeName||"")){r=t.getElementsByTagName("source");for(n=0,s=r.length;n<s;n++){r[n].setAttribute("sizes",i)}}if(!a.detail.dataAttr){Y(e,a.detail)}});var i=function(e,t,a){var i;var r=e.parentNode;if(r){a=s(e,r,a);i=X(e,"lazybeforesizes",{width:a,dataAttr:!!t});if(!i.defaultPrevented){a=i.detail.width;if(a&&a!==e._lazysizesWidth){n(e,r,i,a)}}}};var e=function(){var e;var t=a.length;if(t){e=0;for(;e<t;e++){i(a[e])}}};var t=ie(e);return{_:function(){a=D.getElementsByClassName(H.autosizesClass);q("resize",t)},checkElems:t,updateElem:i}}(),t=function(){if(!t.i&&D.getElementsByClassName){t.i=true;re._();e._()}};return I(function(){H.init&&t()}),k={cfg:H,autoSizer:re,loader:e,init:t,uP:Y,aC:K,rC:Q,hC:J,fire:X,gW:s,rAF:ee}}(e,e.document,Date);e.lazySizes=t,"object"==typeof module&&module.exports&&(module.exports=t)}("undefined"!=typeof window?window:{});;
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"==typeof define&&define.amd?define(t):e.moment=t()}(this,function(){"use strict";var H;function f(){return H.apply(null,arguments)}function a(e){return e instanceof Array||"[object Array]"===Object.prototype.toString.call(e)}function F(e){return null!=e&&"[object Object]"===Object.prototype.toString.call(e)}function c(e,t){return Object.prototype.hasOwnProperty.call(e,t)}function L(e){if(Object.getOwnPropertyNames)return 0===Object.getOwnPropertyNames(e).length;for(var t in e)if(c(e,t))return;return 1}function o(e){return void 0===e}function u(e){return"number"==typeof e||"[object Number]"===Object.prototype.toString.call(e)}function V(e){return e instanceof Date||"[object Date]"===Object.prototype.toString.call(e)}function G(e,t){for(var n=[],s=e.length,i=0;i<s;++i)n.push(t(e[i],i));return n}function E(e,t){for(var n in t)c(t,n)&&(e[n]=t[n]);return c(t,"toString")&&(e.toString=t.toString),c(t,"valueOf")&&(e.valueOf=t.valueOf),e}function l(e,t,n,s){return Pt(e,t,n,s,!0).utc()}function m(e){return null==e._pf&&(e._pf={empty:!1,unusedTokens:[],unusedInput:[],overflow:-2,charsLeftOver:0,nullInput:!1,invalidEra:null,invalidMonth:null,invalidFormat:!1,userInvalidated:!1,iso:!1,parsedDateParts:[],era:null,meridiem:null,rfc2822:!1,weekdayMismatch:!1}),e._pf}function A(e){if(null==e._isValid){var t=m(e),n=j.call(t.parsedDateParts,function(e){return null!=e}),n=!isNaN(e._d.getTime())&&t.overflow<0&&!t.empty&&!t.invalidEra&&!t.invalidMonth&&!t.invalidWeekday&&!t.weekdayMismatch&&!t.nullInput&&!t.invalidFormat&&!t.userInvalidated&&(!t.meridiem||t.meridiem&&n);if(e._strict&&(n=n&&0===t.charsLeftOver&&0===t.unusedTokens.length&&void 0===t.bigHour),null!=Object.isFrozen&&Object.isFrozen(e))return n;e._isValid=n}return e._isValid}function I(e){var t=l(NaN);return null!=e?E(m(t),e):m(t).userInvalidated=!0,t}var j=Array.prototype.some||function(e){for(var t=Object(this),n=t.length>>>0,s=0;s<n;s++)if(s in t&&e.call(this,t[s],s,t))return!0;return!1},Z=f.momentProperties=[],z=!1;function $(e,t){var n,s,i,r=Z.length;if(o(t._isAMomentObject)||(e._isAMomentObject=t._isAMomentObject),o(t._i)||(e._i=t._i),o(t._f)||(e._f=t._f),o(t._l)||(e._l=t._l),o(t._strict)||(e._strict=t._strict),o(t._tzm)||(e._tzm=t._tzm),o(t._isUTC)||(e._isUTC=t._isUTC),o(t._offset)||(e._offset=t._offset),o(t._pf)||(e._pf=m(t)),o(t._locale)||(e._locale=t._locale),0<r)for(n=0;n<r;n++)o(i=t[s=Z[n]])||(e[s]=i);return e}function q(e){$(this,e),this._d=new Date(null!=e._d?e._d.getTime():NaN),this.isValid()||(this._d=new Date(NaN)),!1===z&&(z=!0,f.updateOffset(this),z=!1)}function h(e){return e instanceof q||null!=e&&null!=e._isAMomentObject}function B(e){!1===f.suppressDeprecationWarnings&&"undefined"!=typeof console&&console.warn&&console.warn("Deprecation warning: "+e)}function e(r,a){var o=!0;return E(function(){if(null!=f.deprecationHandler&&f.deprecationHandler(null,r),o){for(var e,t,n=[],s=arguments.length,i=0;i<s;i++){if(e="","object"==typeof arguments[i]){for(t in e+="\n["+i+"] ",arguments[0])c(arguments[0],t)&&(e+=t+": "+arguments[0][t]+", ");e=e.slice(0,-2)}else e=arguments[i];n.push(e)}B(r+"\nArguments: "+Array.prototype.slice.call(n).join("")+"\n"+(new Error).stack),o=!1}return a.apply(this,arguments)},a)}var J={};function Q(e,t){null!=f.deprecationHandler&&f.deprecationHandler(e,t),J[e]||(B(t),J[e]=!0)}function d(e){return"undefined"!=typeof Function&&e instanceof Function||"[object Function]"===Object.prototype.toString.call(e)}function X(e,t){var n,s=E({},e);for(n in t)c(t,n)&&(F(e[n])&&F(t[n])?(s[n]={},E(s[n],e[n]),E(s[n],t[n])):null!=t[n]?s[n]=t[n]:delete s[n]);for(n in e)c(e,n)&&!c(t,n)&&F(e[n])&&(s[n]=E({},s[n]));return s}function K(e){null!=e&&this.set(e)}f.suppressDeprecationWarnings=!1,f.deprecationHandler=null;var ee=Object.keys||function(e){var t,n=[];for(t in e)c(e,t)&&n.push(t);return n};function r(e,t,n){var s=""+Math.abs(e);return(0<=e?n?"+":"":"-")+Math.pow(10,Math.max(0,t-s.length)).toString().substr(1)+s}var te=/(\[[^\[]*\])|(\\)?([Hh]mm(ss)?|Mo|MM?M?M?|Do|DDDo|DD?D?D?|ddd?d?|do?|w[o|w]?|W[o|W]?|Qo?|N{1,5}|YYYYYY|YYYYY|YYYY|YY|y{2,4}|yo?|gg(ggg?)?|GG(GGG?)?|e|E|a|A|hh?|HH?|kk?|mm?|ss?|S{1,9}|x|X|zz?|ZZ?|.)/g,ne=/(\[[^\[]*\])|(\\)?(LTS|LT|LL?L?L?|l{1,4})/g,se={},ie={};function s(e,t,n,s){var i="string"==typeof s?function(){return this[s]()}:s;e&&(ie[e]=i),t&&(ie[t[0]]=function(){return r(i.apply(this,arguments),t[1],t[2])}),n&&(ie[n]=function(){return this.localeData().ordinal(i.apply(this,arguments),e)})}function re(e,t){return e.isValid()?(t=ae(t,e.localeData()),se[t]=se[t]||function(s){for(var e,i=s.match(te),t=0,r=i.length;t<r;t++)ie[i[t]]?i[t]=ie[i[t]]:i[t]=(e=i[t]).match(/\[[\s\S]/)?e.replace(/^\[|\]$/g,""):e.replace(/\\/g,"");return function(e){for(var t="",n=0;n<r;n++)t+=d(i[n])?i[n].call(e,s):i[n];return t}}(t),se[t](e)):e.localeData().invalidDate()}function ae(e,t){var n=5;function s(e){return t.longDateFormat(e)||e}for(ne.lastIndex=0;0<=n&&ne.test(e);)e=e.replace(ne,s),ne.lastIndex=0,--n;return e}var oe={};function t(e,t){var n=e.toLowerCase();oe[n]=oe[n+"s"]=oe[t]=e}function _(e){return"string"==typeof e?oe[e]||oe[e.toLowerCase()]:void 0}function ue(e){var t,n,s={};for(n in e)c(e,n)&&(t=_(n))&&(s[t]=e[n]);return s}var le={};function n(e,t){le[e]=t}function he(e){return e%4==0&&e%100!=0||e%400==0}function y(e){return e<0?Math.ceil(e)||0:Math.floor(e)}function g(e){var e=+e,t=0;return t=0!=e&&isFinite(e)?y(e):t}function de(t,n){return function(e){return null!=e?(fe(this,t,e),f.updateOffset(this,n),this):ce(this,t)}}function ce(e,t){return e.isValid()?e._d["get"+(e._isUTC?"UTC":"")+t]():NaN}function fe(e,t,n){e.isValid()&&!isNaN(n)&&("FullYear"===t&&he(e.year())&&1===e.month()&&29===e.date()?(n=g(n),e._d["set"+(e._isUTC?"UTC":"")+t](n,e.month(),We(n,e.month()))):e._d["set"+(e._isUTC?"UTC":"")+t](n))}var i=/\d/,w=/\d\d/,me=/\d{3}/,_e=/\d{4}/,ye=/[+-]?\d{6}/,p=/\d\d?/,ge=/\d\d\d\d?/,we=/\d\d\d\d\d\d?/,pe=/\d{1,3}/,ve=/\d{1,4}/,ke=/[+-]?\d{1,6}/,Me=/\d+/,De=/[+-]?\d+/,Se=/Z|[+-]\d\d:?\d\d/gi,Ye=/Z|[+-]\d\d(?::?\d\d)?/gi,v=/[0-9]{0,256}['a-z\u00A0-\u05FF\u0700-\uD7FF\uF900-\uFDCF\uFDF0-\uFF07\uFF10-\uFFEF]{1,256}|[\u0600-\u06FF\/]{1,256}(\s*?[\u0600-\u06FF]{1,256}){1,2}/i;function k(e,n,s){be[e]=d(n)?n:function(e,t){return e&&s?s:n}}function Oe(e,t){return c(be,e)?be[e](t._strict,t._locale):new RegExp(M(e.replace("\\","").replace(/\\(\[)|\\(\])|\[([^\]\[]*)\]|\\(.)/g,function(e,t,n,s,i){return t||n||s||i})))}function M(e){return e.replace(/[-\/\\^$*+?.()|[\]{}]/g,"\\$&")}var be={},xe={};function D(e,n){var t,s,i=n;for("string"==typeof e&&(e=[e]),u(n)&&(i=function(e,t){t[n]=g(e)}),s=e.length,t=0;t<s;t++)xe[e[t]]=i}function Te(e,i){D(e,function(e,t,n,s){n._w=n._w||{},i(e,n._w,n,s)})}var S,Y=0,O=1,b=2,x=3,T=4,N=5,Ne=6,Pe=7,Re=8;function We(e,t){if(isNaN(e)||isNaN(t))return NaN;var n=(t%(n=12)+n)%n;return e+=(t-n)/12,1==n?he(e)?29:28:31-n%7%2}S=Array.prototype.indexOf||function(e){for(var t=0;t<this.length;++t)if(this[t]===e)return t;return-1},s("M",["MM",2],"Mo",function(){return this.month()+1}),s("MMM",0,0,function(e){return this.localeData().monthsShort(this,e)}),s("MMMM",0,0,function(e){return this.localeData().months(this,e)}),t("month","M"),n("month",8),k("M",p),k("MM",p,w),k("MMM",function(e,t){return t.monthsShortRegex(e)}),k("MMMM",function(e,t){return t.monthsRegex(e)}),D(["M","MM"],function(e,t){t[O]=g(e)-1}),D(["MMM","MMMM"],function(e,t,n,s){s=n._locale.monthsParse(e,s,n._strict);null!=s?t[O]=s:m(n).invalidMonth=e});var Ce="January_February_March_April_May_June_July_August_September_October_November_December".split("_"),Ue="Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),He=/D[oD]?(\[[^\[\]]*\]|\s)+MMMM?/,Fe=v,Le=v;function Ve(e,t){var n;if(e.isValid()){if("string"==typeof t)if(/^\d+$/.test(t))t=g(t);else if(!u(t=e.localeData().monthsParse(t)))return;n=Math.min(e.date(),We(e.year(),t)),e._d["set"+(e._isUTC?"UTC":"")+"Month"](t,n)}}function Ge(e){return null!=e?(Ve(this,e),f.updateOffset(this,!0),this):ce(this,"Month")}function Ee(){function e(e,t){return t.length-e.length}for(var t,n=[],s=[],i=[],r=0;r<12;r++)t=l([2e3,r]),n.push(this.monthsShort(t,"")),s.push(this.months(t,"")),i.push(this.months(t,"")),i.push(this.monthsShort(t,""));for(n.sort(e),s.sort(e),i.sort(e),r=0;r<12;r++)n[r]=M(n[r]),s[r]=M(s[r]);for(r=0;r<24;r++)i[r]=M(i[r]);this._monthsRegex=new RegExp("^("+i.join("|")+")","i"),this._monthsShortRegex=this._monthsRegex,this._monthsStrictRegex=new RegExp("^("+s.join("|")+")","i"),this._monthsShortStrictRegex=new RegExp("^("+n.join("|")+")","i")}function Ae(e){return he(e)?366:365}s("Y",0,0,function(){var e=this.year();return e<=9999?r(e,4):"+"+e}),s(0,["YY",2],0,function(){return this.year()%100}),s(0,["YYYY",4],0,"year"),s(0,["YYYYY",5],0,"year"),s(0,["YYYYYY",6,!0],0,"year"),t("year","y"),n("year",1),k("Y",De),k("YY",p,w),k("YYYY",ve,_e),k("YYYYY",ke,ye),k("YYYYYY",ke,ye),D(["YYYYY","YYYYYY"],Y),D("YYYY",function(e,t){t[Y]=2===e.length?f.parseTwoDigitYear(e):g(e)}),D("YY",function(e,t){t[Y]=f.parseTwoDigitYear(e)}),D("Y",function(e,t){t[Y]=parseInt(e,10)}),f.parseTwoDigitYear=function(e){return g(e)+(68<g(e)?1900:2e3)};var Ie=de("FullYear",!0);function je(e,t,n,s,i,r,a){var o;return e<100&&0<=e?(o=new Date(e+400,t,n,s,i,r,a),isFinite(o.getFullYear())&&o.setFullYear(e)):o=new Date(e,t,n,s,i,r,a),o}function Ze(e){var t;return e<100&&0<=e?((t=Array.prototype.slice.call(arguments))[0]=e+400,t=new Date(Date.UTC.apply(null,t)),isFinite(t.getUTCFullYear())&&t.setUTCFullYear(e)):t=new Date(Date.UTC.apply(null,arguments)),t}function ze(e,t,n){n=7+t-n;return n-(7+Ze(e,0,n).getUTCDay()-t)%7-1}function $e(e,t,n,s,i){var r,t=1+7*(t-1)+(7+n-s)%7+ze(e,s,i),n=t<=0?Ae(r=e-1)+t:t>Ae(e)?(r=e+1,t-Ae(e)):(r=e,t);return{year:r,dayOfYear:n}}function qe(e,t,n){var s,i,r=ze(e.year(),t,n),r=Math.floor((e.dayOfYear()-r-1)/7)+1;return r<1?s=r+P(i=e.year()-1,t,n):r>P(e.year(),t,n)?(s=r-P(e.year(),t,n),i=e.year()+1):(i=e.year(),s=r),{week:s,year:i}}function P(e,t,n){var s=ze(e,t,n),t=ze(e+1,t,n);return(Ae(e)-s+t)/7}s("w",["ww",2],"wo","week"),s("W",["WW",2],"Wo","isoWeek"),t("week","w"),t("isoWeek","W"),n("week",5),n("isoWeek",5),k("w",p),k("ww",p,w),k("W",p),k("WW",p,w),Te(["w","ww","W","WW"],function(e,t,n,s){t[s.substr(0,1)]=g(e)});function Be(e,t){return e.slice(t,7).concat(e.slice(0,t))}s("d",0,"do","day"),s("dd",0,0,function(e){return this.localeData().weekdaysMin(this,e)}),s("ddd",0,0,function(e){return this.localeData().weekdaysShort(this,e)}),s("dddd",0,0,function(e){return this.localeData().weekdays(this,e)}),s("e",0,0,"weekday"),s("E",0,0,"isoWeekday"),t("day","d"),t("weekday","e"),t("isoWeekday","E"),n("day",11),n("weekday",11),n("isoWeekday",11),k("d",p),k("e",p),k("E",p),k("dd",function(e,t){return t.weekdaysMinRegex(e)}),k("ddd",function(e,t){return t.weekdaysShortRegex(e)}),k("dddd",function(e,t){return t.weekdaysRegex(e)}),Te(["dd","ddd","dddd"],function(e,t,n,s){s=n._locale.weekdaysParse(e,s,n._strict);null!=s?t.d=s:m(n).invalidWeekday=e}),Te(["d","e","E"],function(e,t,n,s){t[s]=g(e)});var Je="Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),Qe="Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),Xe="Su_Mo_Tu_We_Th_Fr_Sa".split("_"),Ke=v,et=v,tt=v;function nt(){function e(e,t){return t.length-e.length}for(var t,n,s,i=[],r=[],a=[],o=[],u=0;u<7;u++)s=l([2e3,1]).day(u),t=M(this.weekdaysMin(s,"")),n=M(this.weekdaysShort(s,"")),s=M(this.weekdays(s,"")),i.push(t),r.push(n),a.push(s),o.push(t),o.push(n),o.push(s);i.sort(e),r.sort(e),a.sort(e),o.sort(e),this._weekdaysRegex=new RegExp("^("+o.join("|")+")","i"),this._weekdaysShortRegex=this._weekdaysRegex,this._weekdaysMinRegex=this._weekdaysRegex,this._weekdaysStrictRegex=new RegExp("^("+a.join("|")+")","i"),this._weekdaysShortStrictRegex=new RegExp("^("+r.join("|")+")","i"),this._weekdaysMinStrictRegex=new RegExp("^("+i.join("|")+")","i")}function st(){return this.hours()%12||12}function it(e,t){s(e,0,0,function(){return this.localeData().meridiem(this.hours(),this.minutes(),t)})}function rt(e,t){return t._meridiemParse}s("H",["HH",2],0,"hour"),s("h",["hh",2],0,st),s("k",["kk",2],0,function(){return this.hours()||24}),s("hmm",0,0,function(){return""+st.apply(this)+r(this.minutes(),2)}),s("hmmss",0,0,function(){return""+st.apply(this)+r(this.minutes(),2)+r(this.seconds(),2)}),s("Hmm",0,0,function(){return""+this.hours()+r(this.minutes(),2)}),s("Hmmss",0,0,function(){return""+this.hours()+r(this.minutes(),2)+r(this.seconds(),2)}),it("a",!0),it("A",!1),t("hour","h"),n("hour",13),k("a",rt),k("A",rt),k("H",p),k("h",p),k("k",p),k("HH",p,w),k("hh",p,w),k("kk",p,w),k("hmm",ge),k("hmmss",we),k("Hmm",ge),k("Hmmss",we),D(["H","HH"],x),D(["k","kk"],function(e,t,n){e=g(e);t[x]=24===e?0:e}),D(["a","A"],function(e,t,n){n._isPm=n._locale.isPM(e),n._meridiem=e}),D(["h","hh"],function(e,t,n){t[x]=g(e),m(n).bigHour=!0}),D("hmm",function(e,t,n){var s=e.length-2;t[x]=g(e.substr(0,s)),t[T]=g(e.substr(s)),m(n).bigHour=!0}),D("hmmss",function(e,t,n){var s=e.length-4,i=e.length-2;t[x]=g(e.substr(0,s)),t[T]=g(e.substr(s,2)),t[N]=g(e.substr(i)),m(n).bigHour=!0}),D("Hmm",function(e,t,n){var s=e.length-2;t[x]=g(e.substr(0,s)),t[T]=g(e.substr(s))}),D("Hmmss",function(e,t,n){var s=e.length-4,i=e.length-2;t[x]=g(e.substr(0,s)),t[T]=g(e.substr(s,2)),t[N]=g(e.substr(i))});v=de("Hours",!0);var at,ot={calendar:{sameDay:"[Today at] LT",nextDay:"[Tomorrow at] LT",nextWeek:"dddd [at] LT",lastDay:"[Yesterday at] LT",lastWeek:"[Last] dddd [at] LT",sameElse:"L"},longDateFormat:{LTS:"h:mm:ss A",LT:"h:mm A",L:"MM/DD/YYYY",LL:"MMMM D, YYYY",LLL:"MMMM D, YYYY h:mm A",LLLL:"dddd, MMMM D, YYYY h:mm A"},invalidDate:"Invalid date",ordinal:"%d",dayOfMonthOrdinalParse:/\d{1,2}/,relativeTime:{future:"in %s",past:"%s ago",s:"a few seconds",ss:"%d seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",w:"a week",ww:"%d weeks",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},months:Ce,monthsShort:Ue,week:{dow:0,doy:6},weekdays:Je,weekdaysMin:Xe,weekdaysShort:Qe,meridiemParse:/[ap]\.?m?\.?/i},R={},ut={};function lt(e){return e&&e.toLowerCase().replace("_","-")}function ht(e){for(var t,n,s,i,r=0;r<e.length;){for(t=(i=lt(e[r]).split("-")).length,n=(n=lt(e[r+1]))?n.split("-"):null;0<t;){if(s=dt(i.slice(0,t).join("-")))return s;if(n&&n.length>=t&&function(e,t){for(var n=Math.min(e.length,t.length),s=0;s<n;s+=1)if(e[s]!==t[s])return s;return n}(i,n)>=t-1)break;t--}r++}return at}function dt(t){var e;if(void 0===R[t]&&"undefined"!=typeof module&&module&&module.exports&&null!=t.match("^[^/\\\\]*$"))try{e=at._abbr,require("./locale/"+t),ct(e)}catch(e){R[t]=null}return R[t]}function ct(e,t){return e&&((t=o(t)?mt(e):ft(e,t))?at=t:"undefined"!=typeof console&&console.warn&&console.warn("Locale "+e+" not found. Did you forget to load it?")),at._abbr}function ft(e,t){if(null===t)return delete R[e],null;var n,s=ot;if(t.abbr=e,null!=R[e])Q("defineLocaleOverride","use moment.updateLocale(localeName, config) to change an existing locale. moment.defineLocale(localeName, config) should only be used for creating a new locale See http://momentjs.com/guides/#/warnings/define-locale/ for more info."),s=R[e]._config;else if(null!=t.parentLocale)if(null!=R[t.parentLocale])s=R[t.parentLocale]._config;else{if(null==(n=dt(t.parentLocale)))return ut[t.parentLocale]||(ut[t.parentLocale]=[]),ut[t.parentLocale].push({name:e,config:t}),null;s=n._config}return R[e]=new K(X(s,t)),ut[e]&&ut[e].forEach(function(e){ft(e.name,e.config)}),ct(e),R[e]}function mt(e){var t;if(!(e=e&&e._locale&&e._locale._abbr?e._locale._abbr:e))return at;if(!a(e)){if(t=dt(e))return t;e=[e]}return ht(e)}function _t(e){var t=e._a;return t&&-2===m(e).overflow&&(t=t[O]<0||11<t[O]?O:t[b]<1||t[b]>We(t[Y],t[O])?b:t[x]<0||24<t[x]||24===t[x]&&(0!==t[T]||0!==t[N]||0!==t[Ne])?x:t[T]<0||59<t[T]?T:t[N]<0||59<t[N]?N:t[Ne]<0||999<t[Ne]?Ne:-1,m(e)._overflowDayOfYear&&(t<Y||b<t)&&(t=b),m(e)._overflowWeeks&&-1===t&&(t=Pe),m(e)._overflowWeekday&&-1===t&&(t=Re),m(e).overflow=t),e}var yt=/^\s*((?:[+-]\d{6}|\d{4})-(?:\d\d-\d\d|W\d\d-\d|W\d\d|\d\d\d|\d\d))(?:(T| )(\d\d(?::\d\d(?::\d\d(?:[.,]\d+)?)?)?)([+-]\d\d(?::?\d\d)?|\s*Z)?)?$/,gt=/^\s*((?:[+-]\d{6}|\d{4})(?:\d\d\d\d|W\d\d\d|W\d\d|\d\d\d|\d\d|))(?:(T| )(\d\d(?:\d\d(?:\d\d(?:[.,]\d+)?)?)?)([+-]\d\d(?::?\d\d)?|\s*Z)?)?$/,wt=/Z|[+-]\d\d(?::?\d\d)?/,pt=[["YYYYYY-MM-DD",/[+-]\d{6}-\d\d-\d\d/],["YYYY-MM-DD",/\d{4}-\d\d-\d\d/],["GGGG-[W]WW-E",/\d{4}-W\d\d-\d/],["GGGG-[W]WW",/\d{4}-W\d\d/,!1],["YYYY-DDD",/\d{4}-\d{3}/],["YYYY-MM",/\d{4}-\d\d/,!1],["YYYYYYMMDD",/[+-]\d{10}/],["YYYYMMDD",/\d{8}/],["GGGG[W]WWE",/\d{4}W\d{3}/],["GGGG[W]WW",/\d{4}W\d{2}/,!1],["YYYYDDD",/\d{7}/],["YYYYMM",/\d{6}/,!1],["YYYY",/\d{4}/,!1]],vt=[["HH:mm:ss.SSSS",/\d\d:\d\d:\d\d\.\d+/],["HH:mm:ss,SSSS",/\d\d:\d\d:\d\d,\d+/],["HH:mm:ss",/\d\d:\d\d:\d\d/],["HH:mm",/\d\d:\d\d/],["HHmmss.SSSS",/\d\d\d\d\d\d\.\d+/],["HHmmss,SSSS",/\d\d\d\d\d\d,\d+/],["HHmmss",/\d\d\d\d\d\d/],["HHmm",/\d\d\d\d/],["HH",/\d\d/]],kt=/^\/?Date\((-?\d+)/i,Mt=/^(?:(Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s)?(\d{1,2})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d{2,4})\s(\d\d):(\d\d)(?::(\d\d))?\s(?:(UT|GMT|[ECMP][SD]T)|([Zz])|([+-]\d{4}))$/,Dt={UT:0,GMT:0,EDT:-240,EST:-300,CDT:-300,CST:-360,MDT:-360,MST:-420,PDT:-420,PST:-480};function St(e){var t,n,s,i,r,a,o=e._i,u=yt.exec(o)||gt.exec(o),o=pt.length,l=vt.length;if(u){for(m(e).iso=!0,t=0,n=o;t<n;t++)if(pt[t][1].exec(u[1])){i=pt[t][0],s=!1!==pt[t][2];break}if(null==i)e._isValid=!1;else{if(u[3]){for(t=0,n=l;t<n;t++)if(vt[t][1].exec(u[3])){r=(u[2]||" ")+vt[t][0];break}if(null==r)return void(e._isValid=!1)}if(s||null==r){if(u[4]){if(!wt.exec(u[4]))return void(e._isValid=!1);a="Z"}e._f=i+(r||"")+(a||""),Tt(e)}else e._isValid=!1}}else e._isValid=!1}function Yt(e,t,n,s,i,r){e=[function(e){e=parseInt(e,10);{if(e<=49)return 2e3+e;if(e<=999)return 1900+e}return e}(e),Ue.indexOf(t),parseInt(n,10),parseInt(s,10),parseInt(i,10)];return r&&e.push(parseInt(r,10)),e}function Ot(e){var t,n,s,i,r=Mt.exec(e._i.replace(/\([^()]*\)|[\n\t]/g," ").replace(/(\s\s+)/g," ").replace(/^\s\s*/,"").replace(/\s\s*$/,""));r?(t=Yt(r[4],r[3],r[2],r[5],r[6],r[7]),n=r[1],s=t,i=e,n&&Qe.indexOf(n)!==new Date(s[0],s[1],s[2]).getDay()?(m(i).weekdayMismatch=!0,i._isValid=!1):(e._a=t,e._tzm=(n=r[8],s=r[9],i=r[10],n?Dt[n]:s?0:60*(((n=parseInt(i,10))-(s=n%100))/100)+s),e._d=Ze.apply(null,e._a),e._d.setUTCMinutes(e._d.getUTCMinutes()-e._tzm),m(e).rfc2822=!0)):e._isValid=!1}function bt(e,t,n){return null!=e?e:null!=t?t:n}function xt(e){var t,n,s,i,r,a,o,u,l,h,d,c=[];if(!e._d){for(s=e,i=new Date(f.now()),n=s._useUTC?[i.getUTCFullYear(),i.getUTCMonth(),i.getUTCDate()]:[i.getFullYear(),i.getMonth(),i.getDate()],e._w&&null==e._a[b]&&null==e._a[O]&&(null!=(i=(s=e)._w).GG||null!=i.W||null!=i.E?(u=1,l=4,r=bt(i.GG,s._a[Y],qe(W(),1,4).year),a=bt(i.W,1),((o=bt(i.E,1))<1||7<o)&&(h=!0)):(u=s._locale._week.dow,l=s._locale._week.doy,d=qe(W(),u,l),r=bt(i.gg,s._a[Y],d.year),a=bt(i.w,d.week),null!=i.d?((o=i.d)<0||6<o)&&(h=!0):null!=i.e?(o=i.e+u,(i.e<0||6<i.e)&&(h=!0)):o=u),a<1||a>P(r,u,l)?m(s)._overflowWeeks=!0:null!=h?m(s)._overflowWeekday=!0:(d=$e(r,a,o,u,l),s._a[Y]=d.year,s._dayOfYear=d.dayOfYear)),null!=e._dayOfYear&&(i=bt(e._a[Y],n[Y]),(e._dayOfYear>Ae(i)||0===e._dayOfYear)&&(m(e)._overflowDayOfYear=!0),h=Ze(i,0,e._dayOfYear),e._a[O]=h.getUTCMonth(),e._a[b]=h.getUTCDate()),t=0;t<3&&null==e._a[t];++t)e._a[t]=c[t]=n[t];for(;t<7;t++)e._a[t]=c[t]=null==e._a[t]?2===t?1:0:e._a[t];24===e._a[x]&&0===e._a[T]&&0===e._a[N]&&0===e._a[Ne]&&(e._nextDay=!0,e._a[x]=0),e._d=(e._useUTC?Ze:je).apply(null,c),r=e._useUTC?e._d.getUTCDay():e._d.getDay(),null!=e._tzm&&e._d.setUTCMinutes(e._d.getUTCMinutes()-e._tzm),e._nextDay&&(e._a[x]=24),e._w&&void 0!==e._w.d&&e._w.d!==r&&(m(e).weekdayMismatch=!0)}}function Tt(e){if(e._f===f.ISO_8601)St(e);else if(e._f===f.RFC_2822)Ot(e);else{e._a=[],m(e).empty=!0;for(var t,n,s,i,r,a=""+e._i,o=a.length,u=0,l=ae(e._f,e._locale).match(te)||[],h=l.length,d=0;d<h;d++)n=l[d],(t=(a.match(Oe(n,e))||[])[0])&&(0<(s=a.substr(0,a.indexOf(t))).length&&m(e).unusedInput.push(s),a=a.slice(a.indexOf(t)+t.length),u+=t.length),ie[n]?(t?m(e).empty=!1:m(e).unusedTokens.push(n),s=n,r=e,null!=(i=t)&&c(xe,s)&&xe[s](i,r._a,r,s)):e._strict&&!t&&m(e).unusedTokens.push(n);m(e).charsLeftOver=o-u,0<a.length&&m(e).unusedInput.push(a),e._a[x]<=12&&!0===m(e).bigHour&&0<e._a[x]&&(m(e).bigHour=void 0),m(e).parsedDateParts=e._a.slice(0),m(e).meridiem=e._meridiem,e._a[x]=function(e,t,n){if(null==n)return t;return null!=e.meridiemHour?e.meridiemHour(t,n):null!=e.isPM?((e=e.isPM(n))&&t<12&&(t+=12),t=e||12!==t?t:0):t}(e._locale,e._a[x],e._meridiem),null!==(o=m(e).era)&&(e._a[Y]=e._locale.erasConvertYear(o,e._a[Y])),xt(e),_t(e)}}function Nt(e){var t,n,s,i=e._i,r=e._f;if(e._locale=e._locale||mt(e._l),null===i||void 0===r&&""===i)return I({nullInput:!0});if("string"==typeof i&&(e._i=i=e._locale.preparse(i)),h(i))return new q(_t(i));if(V(i))e._d=i;else if(a(r))!function(e){var t,n,s,i,r,a,o=!1,u=e._f.length;if(0===u)return m(e).invalidFormat=!0,e._d=new Date(NaN);for(i=0;i<u;i++)r=0,a=!1,t=$({},e),null!=e._useUTC&&(t._useUTC=e._useUTC),t._f=e._f[i],Tt(t),A(t)&&(a=!0),r=(r+=m(t).charsLeftOver)+10*m(t).unusedTokens.length,m(t).score=r,o?r<s&&(s=r,n=t):(null==s||r<s||a)&&(s=r,n=t,a&&(o=!0));E(e,n||t)}(e);else if(r)Tt(e);else if(o(r=(i=e)._i))i._d=new Date(f.now());else V(r)?i._d=new Date(r.valueOf()):"string"==typeof r?(n=i,null!==(t=kt.exec(n._i))?n._d=new Date(+t[1]):(St(n),!1===n._isValid&&(delete n._isValid,Ot(n),!1===n._isValid&&(delete n._isValid,n._strict?n._isValid=!1:f.createFromInputFallback(n))))):a(r)?(i._a=G(r.slice(0),function(e){return parseInt(e,10)}),xt(i)):F(r)?(t=i)._d||(s=void 0===(n=ue(t._i)).day?n.date:n.day,t._a=G([n.year,n.month,s,n.hour,n.minute,n.second,n.millisecond],function(e){return e&&parseInt(e,10)}),xt(t)):u(r)?i._d=new Date(r):f.createFromInputFallback(i);return A(e)||(e._d=null),e}function Pt(e,t,n,s,i){var r={};return!0!==t&&!1!==t||(s=t,t=void 0),!0!==n&&!1!==n||(s=n,n=void 0),(F(e)&&L(e)||a(e)&&0===e.length)&&(e=void 0),r._isAMomentObject=!0,r._useUTC=r._isUTC=i,r._l=n,r._i=e,r._f=t,r._strict=s,(i=new q(_t(Nt(i=r))))._nextDay&&(i.add(1,"d"),i._nextDay=void 0),i}function W(e,t,n,s){return Pt(e,t,n,s,!1)}f.createFromInputFallback=e("value provided is not in a recognized RFC2822 or ISO format. moment construction falls back to js Date(), which is not reliable across all browsers and versions. Non RFC2822/ISO date formats are discouraged. Please refer to http://momentjs.com/guides/#/warnings/js-date/ for more info.",function(e){e._d=new Date(e._i+(e._useUTC?" UTC":""))}),f.ISO_8601=function(){},f.RFC_2822=function(){};ge=e("moment().min is deprecated, use moment.max instead. http://momentjs.com/guides/#/warnings/min-max/",function(){var e=W.apply(null,arguments);return this.isValid()&&e.isValid()?e<this?this:e:I()}),we=e("moment().max is deprecated, use moment.min instead. http://momentjs.com/guides/#/warnings/min-max/",function(){var e=W.apply(null,arguments);return this.isValid()&&e.isValid()?this<e?this:e:I()});function Rt(e,t){var n,s;if(!(t=1===t.length&&a(t[0])?t[0]:t).length)return W();for(n=t[0],s=1;s<t.length;++s)t[s].isValid()&&!t[s][e](n)||(n=t[s]);return n}var Wt=["year","quarter","month","week","day","hour","minute","second","millisecond"];function Ct(e){var e=ue(e),t=e.year||0,n=e.quarter||0,s=e.month||0,i=e.week||e.isoWeek||0,r=e.day||0,a=e.hour||0,o=e.minute||0,u=e.second||0,l=e.millisecond||0;this._isValid=function(e){var t,n,s=!1,i=Wt.length;for(t in e)if(c(e,t)&&(-1===S.call(Wt,t)||null!=e[t]&&isNaN(e[t])))return!1;for(n=0;n<i;++n)if(e[Wt[n]]){if(s)return!1;parseFloat(e[Wt[n]])!==g(e[Wt[n]])&&(s=!0)}return!0}(e),this._milliseconds=+l+1e3*u+6e4*o+1e3*a*60*60,this._days=+r+7*i,this._months=+s+3*n+12*t,this._data={},this._locale=mt(),this._bubble()}function Ut(e){return e instanceof Ct}function Ht(e){return e<0?-1*Math.round(-1*e):Math.round(e)}function Ft(e,n){s(e,0,0,function(){var e=this.utcOffset(),t="+";return e<0&&(e=-e,t="-"),t+r(~~(e/60),2)+n+r(~~e%60,2)})}Ft("Z",":"),Ft("ZZ",""),k("Z",Ye),k("ZZ",Ye),D(["Z","ZZ"],function(e,t,n){n._useUTC=!0,n._tzm=Vt(Ye,e)});var Lt=/([\+\-]|\d\d)/gi;function Vt(e,t){var t=(t||"").match(e);return null===t?null:0===(t=60*(e=((t[t.length-1]||[])+"").match(Lt)||["-",0,0])[1]+g(e[2]))?0:"+"===e[0]?t:-t}function Gt(e,t){var n;return t._isUTC?(t=t.clone(),n=(h(e)||V(e)?e:W(e)).valueOf()-t.valueOf(),t._d.setTime(t._d.valueOf()+n),f.updateOffset(t,!1),t):W(e).local()}function Et(e){return-Math.round(e._d.getTimezoneOffset())}function At(){return!!this.isValid()&&(this._isUTC&&0===this._offset)}f.updateOffset=function(){};var It=/^(-|\+)?(?:(\d*)[. ])?(\d+):(\d+)(?::(\d+)(\.\d*)?)?$/,jt=/^(-|\+)?P(?:([-+]?[0-9,.]*)Y)?(?:([-+]?[0-9,.]*)M)?(?:([-+]?[0-9,.]*)W)?(?:([-+]?[0-9,.]*)D)?(?:T(?:([-+]?[0-9,.]*)H)?(?:([-+]?[0-9,.]*)M)?(?:([-+]?[0-9,.]*)S)?)?$/;function C(e,t){var n,s=e,i=null;return Ut(e)?s={ms:e._milliseconds,d:e._days,M:e._months}:u(e)||!isNaN(+e)?(s={},t?s[t]=+e:s.milliseconds=+e):(i=It.exec(e))?(n="-"===i[1]?-1:1,s={y:0,d:g(i[b])*n,h:g(i[x])*n,m:g(i[T])*n,s:g(i[N])*n,ms:g(Ht(1e3*i[Ne]))*n}):(i=jt.exec(e))?(n="-"===i[1]?-1:1,s={y:Zt(i[2],n),M:Zt(i[3],n),w:Zt(i[4],n),d:Zt(i[5],n),h:Zt(i[6],n),m:Zt(i[7],n),s:Zt(i[8],n)}):null==s?s={}:"object"==typeof s&&("from"in s||"to"in s)&&(t=function(e,t){var n;if(!e.isValid()||!t.isValid())return{milliseconds:0,months:0};t=Gt(t,e),e.isBefore(t)?n=zt(e,t):((n=zt(t,e)).milliseconds=-n.milliseconds,n.months=-n.months);return n}(W(s.from),W(s.to)),(s={}).ms=t.milliseconds,s.M=t.months),i=new Ct(s),Ut(e)&&c(e,"_locale")&&(i._locale=e._locale),Ut(e)&&c(e,"_isValid")&&(i._isValid=e._isValid),i}function Zt(e,t){e=e&&parseFloat(e.replace(",","."));return(isNaN(e)?0:e)*t}function zt(e,t){var n={};return n.months=t.month()-e.month()+12*(t.year()-e.year()),e.clone().add(n.months,"M").isAfter(t)&&--n.months,n.milliseconds=+t-+e.clone().add(n.months,"M"),n}function $t(s,i){return function(e,t){var n;return null===t||isNaN(+t)||(Q(i,"moment()."+i+"(period, number) is deprecated. Please use moment()."+i+"(number, period). See http://momentjs.com/guides/#/warnings/add-inverted-param/ for more info."),n=e,e=t,t=n),qt(this,C(e,t),s),this}}function qt(e,t,n,s){var i=t._milliseconds,r=Ht(t._days),t=Ht(t._months);e.isValid()&&(s=null==s||s,t&&Ve(e,ce(e,"Month")+t*n),r&&fe(e,"Date",ce(e,"Date")+r*n),i&&e._d.setTime(e._d.valueOf()+i*n),s&&f.updateOffset(e,r||t))}C.fn=Ct.prototype,C.invalid=function(){return C(NaN)};Ce=$t(1,"add"),Je=$t(-1,"subtract");function Bt(e){return"string"==typeof e||e instanceof String}function Jt(e){return h(e)||V(e)||Bt(e)||u(e)||function(t){var e=a(t),n=!1;e&&(n=0===t.filter(function(e){return!u(e)&&Bt(t)}).length);return e&&n}(e)||function(e){var t,n,s=F(e)&&!L(e),i=!1,r=["years","year","y","months","month","M","days","day","d","dates","date","D","hours","hour","h","minutes","minute","m","seconds","second","s","milliseconds","millisecond","ms"],a=r.length;for(t=0;t<a;t+=1)n=r[t],i=i||c(e,n);return s&&i}(e)||null==e}function Qt(e,t){if(e.date()<t.date())return-Qt(t,e);var n=12*(t.year()-e.year())+(t.month()-e.month()),s=e.clone().add(n,"months"),t=t-s<0?(t-s)/(s-e.clone().add(n-1,"months")):(t-s)/(e.clone().add(1+n,"months")-s);return-(n+t)||0}function Xt(e){return void 0===e?this._locale._abbr:(null!=(e=mt(e))&&(this._locale=e),this)}f.defaultFormat="YYYY-MM-DDTHH:mm:ssZ",f.defaultFormatUtc="YYYY-MM-DDTHH:mm:ss[Z]";Xe=e("moment().lang() is deprecated. Instead, use moment().localeData() to get the language configuration. Use moment().locale() to change languages.",function(e){return void 0===e?this.localeData():this.locale(e)});function Kt(){return this._locale}var en=126227808e5;function tn(e,t){return(e%t+t)%t}function nn(e,t,n){return e<100&&0<=e?new Date(e+400,t,n)-en:new Date(e,t,n).valueOf()}function sn(e,t,n){return e<100&&0<=e?Date.UTC(e+400,t,n)-en:Date.UTC(e,t,n)}function rn(e,t){return t.erasAbbrRegex(e)}function an(){for(var e=[],t=[],n=[],s=[],i=this.eras(),r=0,a=i.length;r<a;++r)t.push(M(i[r].name)),e.push(M(i[r].abbr)),n.push(M(i[r].narrow)),s.push(M(i[r].name)),s.push(M(i[r].abbr)),s.push(M(i[r].narrow));this._erasRegex=new RegExp("^("+s.join("|")+")","i"),this._erasNameRegex=new RegExp("^("+t.join("|")+")","i"),this._erasAbbrRegex=new RegExp("^("+e.join("|")+")","i"),this._erasNarrowRegex=new RegExp("^("+n.join("|")+")","i")}function on(e,t){s(0,[e,e.length],0,t)}function un(e,t,n,s,i){var r;return null==e?qe(this,s,i).year:(r=P(e,s,i),function(e,t,n,s,i){e=$e(e,t,n,s,i),t=Ze(e.year,0,e.dayOfYear);return this.year(t.getUTCFullYear()),this.month(t.getUTCMonth()),this.date(t.getUTCDate()),this}.call(this,e,t=r<t?r:t,n,s,i))}s("N",0,0,"eraAbbr"),s("NN",0,0,"eraAbbr"),s("NNN",0,0,"eraAbbr"),s("NNNN",0,0,"eraName"),s("NNNNN",0,0,"eraNarrow"),s("y",["y",1],"yo","eraYear"),s("y",["yy",2],0,"eraYear"),s("y",["yyy",3],0,"eraYear"),s("y",["yyyy",4],0,"eraYear"),k("N",rn),k("NN",rn),k("NNN",rn),k("NNNN",function(e,t){return t.erasNameRegex(e)}),k("NNNNN",function(e,t){return t.erasNarrowRegex(e)}),D(["N","NN","NNN","NNNN","NNNNN"],function(e,t,n,s){s=n._locale.erasParse(e,s,n._strict);s?m(n).era=s:m(n).invalidEra=e}),k("y",Me),k("yy",Me),k("yyy",Me),k("yyyy",Me),k("yo",function(e,t){return t._eraYearOrdinalRegex||Me}),D(["y","yy","yyy","yyyy"],Y),D(["yo"],function(e,t,n,s){var i;n._locale._eraYearOrdinalRegex&&(i=e.match(n._locale._eraYearOrdinalRegex)),n._locale.eraYearOrdinalParse?t[Y]=n._locale.eraYearOrdinalParse(e,i):t[Y]=parseInt(e,10)}),s(0,["gg",2],0,function(){return this.weekYear()%100}),s(0,["GG",2],0,function(){return this.isoWeekYear()%100}),on("gggg","weekYear"),on("ggggg","weekYear"),on("GGGG","isoWeekYear"),on("GGGGG","isoWeekYear"),t("weekYear","gg"),t("isoWeekYear","GG"),n("weekYear",1),n("isoWeekYear",1),k("G",De),k("g",De),k("GG",p,w),k("gg",p,w),k("GGGG",ve,_e),k("gggg",ve,_e),k("GGGGG",ke,ye),k("ggggg",ke,ye),Te(["gggg","ggggg","GGGG","GGGGG"],function(e,t,n,s){t[s.substr(0,2)]=g(e)}),Te(["gg","GG"],function(e,t,n,s){t[s]=f.parseTwoDigitYear(e)}),s("Q",0,"Qo","quarter"),t("quarter","Q"),n("quarter",7),k("Q",i),D("Q",function(e,t){t[O]=3*(g(e)-1)}),s("D",["DD",2],"Do","date"),t("date","D"),n("date",9),k("D",p),k("DD",p,w),k("Do",function(e,t){return e?t._dayOfMonthOrdinalParse||t._ordinalParse:t._dayOfMonthOrdinalParseLenient}),D(["D","DD"],b),D("Do",function(e,t){t[b]=g(e.match(p)[0])});ve=de("Date",!0);s("DDD",["DDDD",3],"DDDo","dayOfYear"),t("dayOfYear","DDD"),n("dayOfYear",4),k("DDD",pe),k("DDDD",me),D(["DDD","DDDD"],function(e,t,n){n._dayOfYear=g(e)}),s("m",["mm",2],0,"minute"),t("minute","m"),n("minute",14),k("m",p),k("mm",p,w),D(["m","mm"],T);var ln,_e=de("Minutes",!1),ke=(s("s",["ss",2],0,"second"),t("second","s"),n("second",15),k("s",p),k("ss",p,w),D(["s","ss"],N),de("Seconds",!1));for(s("S",0,0,function(){return~~(this.millisecond()/100)}),s(0,["SS",2],0,function(){return~~(this.millisecond()/10)}),s(0,["SSS",3],0,"millisecond"),s(0,["SSSS",4],0,function(){return 10*this.millisecond()}),s(0,["SSSSS",5],0,function(){return 100*this.millisecond()}),s(0,["SSSSSS",6],0,function(){return 1e3*this.millisecond()}),s(0,["SSSSSSS",7],0,function(){return 1e4*this.millisecond()}),s(0,["SSSSSSSS",8],0,function(){return 1e5*this.millisecond()}),s(0,["SSSSSSSSS",9],0,function(){return 1e6*this.millisecond()}),t("millisecond","ms"),n("millisecond",16),k("S",pe,i),k("SS",pe,w),k("SSS",pe,me),ln="SSSS";ln.length<=9;ln+="S")k(ln,Me);function hn(e,t){t[Ne]=g(1e3*("0."+e))}for(ln="S";ln.length<=9;ln+="S")D(ln,hn);ye=de("Milliseconds",!1),s("z",0,0,"zoneAbbr"),s("zz",0,0,"zoneName");i=q.prototype;function dn(e){return e}i.add=Ce,i.calendar=function(e,t){1===arguments.length&&(arguments[0]?Jt(arguments[0])?(e=arguments[0],t=void 0):function(e){for(var t=F(e)&&!L(e),n=!1,s=["sameDay","nextDay","lastDay","nextWeek","lastWeek","sameElse"],i=0;i<s.length;i+=1)n=n||c(e,s[i]);return t&&n}(arguments[0])&&(t=arguments[0],e=void 0):t=e=void 0);var e=e||W(),n=Gt(e,this).startOf("day"),n=f.calendarFormat(this,n)||"sameElse",t=t&&(d(t[n])?t[n].call(this,e):t[n]);return this.format(t||this.localeData().calendar(n,this,W(e)))},i.clone=function(){return new q(this)},i.diff=function(e,t,n){var s,i,r;if(!this.isValid())return NaN;if(!(s=Gt(e,this)).isValid())return NaN;switch(i=6e4*(s.utcOffset()-this.utcOffset()),t=_(t)){case"year":r=Qt(this,s)/12;break;case"month":r=Qt(this,s);break;case"quarter":r=Qt(this,s)/3;break;case"second":r=(this-s)/1e3;break;case"minute":r=(this-s)/6e4;break;case"hour":r=(this-s)/36e5;break;case"day":r=(this-s-i)/864e5;break;case"week":r=(this-s-i)/6048e5;break;default:r=this-s}return n?r:y(r)},i.endOf=function(e){var t,n;if(void 0===(e=_(e))||"millisecond"===e||!this.isValid())return this;switch(n=this._isUTC?sn:nn,e){case"year":t=n(this.year()+1,0,1)-1;break;case"quarter":t=n(this.year(),this.month()-this.month()%3+3,1)-1;break;case"month":t=n(this.year(),this.month()+1,1)-1;break;case"week":t=n(this.year(),this.month(),this.date()-this.weekday()+7)-1;break;case"isoWeek":t=n(this.year(),this.month(),this.date()-(this.isoWeekday()-1)+7)-1;break;case"day":case"date":t=n(this.year(),this.month(),this.date()+1)-1;break;case"hour":t=this._d.valueOf(),t+=36e5-tn(t+(this._isUTC?0:6e4*this.utcOffset()),36e5)-1;break;case"minute":t=this._d.valueOf(),t+=6e4-tn(t,6e4)-1;break;case"second":t=this._d.valueOf(),t+=1e3-tn(t,1e3)-1}return this._d.setTime(t),f.updateOffset(this,!0),this},i.format=function(e){return e=e||(this.isUtc()?f.defaultFormatUtc:f.defaultFormat),e=re(this,e),this.localeData().postformat(e)},i.from=function(e,t){return this.isValid()&&(h(e)&&e.isValid()||W(e).isValid())?C({to:this,from:e}).locale(this.locale()).humanize(!t):this.localeData().invalidDate()},i.fromNow=function(e){return this.from(W(),e)},i.to=function(e,t){return this.isValid()&&(h(e)&&e.isValid()||W(e).isValid())?C({from:this,to:e}).locale(this.locale()).humanize(!t):this.localeData().invalidDate()},i.toNow=function(e){return this.to(W(),e)},i.get=function(e){return d(this[e=_(e)])?this[e]():this},i.invalidAt=function(){return m(this).overflow},i.isAfter=function(e,t){return e=h(e)?e:W(e),!(!this.isValid()||!e.isValid())&&("millisecond"===(t=_(t)||"millisecond")?this.valueOf()>e.valueOf():e.valueOf()<this.clone().startOf(t).valueOf())},i.isBefore=function(e,t){return e=h(e)?e:W(e),!(!this.isValid()||!e.isValid())&&("millisecond"===(t=_(t)||"millisecond")?this.valueOf()<e.valueOf():this.clone().endOf(t).valueOf()<e.valueOf())},i.isBetween=function(e,t,n,s){return e=h(e)?e:W(e),t=h(t)?t:W(t),!!(this.isValid()&&e.isValid()&&t.isValid())&&(("("===(s=s||"()")[0]?this.isAfter(e,n):!this.isBefore(e,n))&&(")"===s[1]?this.isBefore(t,n):!this.isAfter(t,n)))},i.isSame=function(e,t){var e=h(e)?e:W(e);return!(!this.isValid()||!e.isValid())&&("millisecond"===(t=_(t)||"millisecond")?this.valueOf()===e.valueOf():(e=e.valueOf(),this.clone().startOf(t).valueOf()<=e&&e<=this.clone().endOf(t).valueOf()))},i.isSameOrAfter=function(e,t){return this.isSame(e,t)||this.isAfter(e,t)},i.isSameOrBefore=function(e,t){return this.isSame(e,t)||this.isBefore(e,t)},i.isValid=function(){return A(this)},i.lang=Xe,i.locale=Xt,i.localeData=Kt,i.max=we,i.min=ge,i.parsingFlags=function(){return E({},m(this))},i.set=function(e,t){if("object"==typeof e)for(var n=function(e){var t,n=[];for(t in e)c(e,t)&&n.push({unit:t,priority:le[t]});return n.sort(function(e,t){return e.priority-t.priority}),n}(e=ue(e)),s=n.length,i=0;i<s;i++)this[n[i].unit](e[n[i].unit]);else if(d(this[e=_(e)]))return this[e](t);return this},i.startOf=function(e){var t,n;if(void 0===(e=_(e))||"millisecond"===e||!this.isValid())return this;switch(n=this._isUTC?sn:nn,e){case"year":t=n(this.year(),0,1);break;case"quarter":t=n(this.year(),this.month()-this.month()%3,1);break;case"month":t=n(this.year(),this.month(),1);break;case"week":t=n(this.year(),this.month(),this.date()-this.weekday());break;case"isoWeek":t=n(this.year(),this.month(),this.date()-(this.isoWeekday()-1));break;case"day":case"date":t=n(this.year(),this.month(),this.date());break;case"hour":t=this._d.valueOf(),t-=tn(t+(this._isUTC?0:6e4*this.utcOffset()),36e5);break;case"minute":t=this._d.valueOf(),t-=tn(t,6e4);break;case"second":t=this._d.valueOf(),t-=tn(t,1e3)}return this._d.setTime(t),f.updateOffset(this,!0),this},i.subtract=Je,i.toArray=function(){var e=this;return[e.year(),e.month(),e.date(),e.hour(),e.minute(),e.second(),e.millisecond()]},i.toObject=function(){var e=this;return{years:e.year(),months:e.month(),date:e.date(),hours:e.hours(),minutes:e.minutes(),seconds:e.seconds(),milliseconds:e.milliseconds()}},i.toDate=function(){return new Date(this.valueOf())},i.toISOString=function(e){if(!this.isValid())return null;var t=(e=!0!==e)?this.clone().utc():this;return t.year()<0||9999<t.year()?re(t,e?"YYYYYY-MM-DD[T]HH:mm:ss.SSS[Z]":"YYYYYY-MM-DD[T]HH:mm:ss.SSSZ"):d(Date.prototype.toISOString)?e?this.toDate().toISOString():new Date(this.valueOf()+60*this.utcOffset()*1e3).toISOString().replace("Z",re(t,"Z")):re(t,e?"YYYY-MM-DD[T]HH:mm:ss.SSS[Z]":"YYYY-MM-DD[T]HH:mm:ss.SSSZ")},i.inspect=function(){if(!this.isValid())return"moment.invalid(/* "+this._i+" */)";var e,t="moment",n="";return this.isLocal()||(t=0===this.utcOffset()?"moment.utc":"moment.parseZone",n="Z"),t="["+t+'("]',e=0<=this.year()&&this.year()<=9999?"YYYY":"YYYYYY",this.format(t+e+"-MM-DD[T]HH:mm:ss.SSS"+(n+'[")]'))},"undefined"!=typeof Symbol&&null!=Symbol.for&&(i[Symbol.for("nodejs.util.inspect.custom")]=function(){return"Moment<"+this.format()+">"}),i.toJSON=function(){return this.isValid()?this.toISOString():null},i.toString=function(){return this.clone().locale("en").format("ddd MMM DD YYYY HH:mm:ss [GMT]ZZ")},i.unix=function(){return Math.floor(this.valueOf()/1e3)},i.valueOf=function(){return this._d.valueOf()-6e4*(this._offset||0)},i.creationData=function(){return{input:this._i,format:this._f,locale:this._locale,isUTC:this._isUTC,strict:this._strict}},i.eraName=function(){for(var e,t=this.localeData().eras(),n=0,s=t.length;n<s;++n){if(e=this.clone().startOf("day").valueOf(),t[n].since<=e&&e<=t[n].until)return t[n].name;if(t[n].until<=e&&e<=t[n].since)return t[n].name}return""},i.eraNarrow=function(){for(var e,t=this.localeData().eras(),n=0,s=t.length;n<s;++n){if(e=this.clone().startOf("day").valueOf(),t[n].since<=e&&e<=t[n].until)return t[n].narrow;if(t[n].until<=e&&e<=t[n].since)return t[n].narrow}return""},i.eraAbbr=function(){for(var e,t=this.localeData().eras(),n=0,s=t.length;n<s;++n){if(e=this.clone().startOf("day").valueOf(),t[n].since<=e&&e<=t[n].until)return t[n].abbr;if(t[n].until<=e&&e<=t[n].since)return t[n].abbr}return""},i.eraYear=function(){for(var e,t,n=this.localeData().eras(),s=0,i=n.length;s<i;++s)if(e=n[s].since<=n[s].until?1:-1,t=this.clone().startOf("day").valueOf(),n[s].since<=t&&t<=n[s].until||n[s].until<=t&&t<=n[s].since)return(this.year()-f(n[s].since).year())*e+n[s].offset;return this.year()},i.year=Ie,i.isLeapYear=function(){return he(this.year())},i.weekYear=function(e){return un.call(this,e,this.week(),this.weekday(),this.localeData()._week.dow,this.localeData()._week.doy)},i.isoWeekYear=function(e){return un.call(this,e,this.isoWeek(),this.isoWeekday(),1,4)},i.quarter=i.quarters=function(e){return null==e?Math.ceil((this.month()+1)/3):this.month(3*(e-1)+this.month()%3)},i.month=Ge,i.daysInMonth=function(){return We(this.year(),this.month())},i.week=i.weeks=function(e){var t=this.localeData().week(this);return null==e?t:this.add(7*(e-t),"d")},i.isoWeek=i.isoWeeks=function(e){var t=qe(this,1,4).week;return null==e?t:this.add(7*(e-t),"d")},i.weeksInYear=function(){var e=this.localeData()._week;return P(this.year(),e.dow,e.doy)},i.weeksInWeekYear=function(){var e=this.localeData()._week;return P(this.weekYear(),e.dow,e.doy)},i.isoWeeksInYear=function(){return P(this.year(),1,4)},i.isoWeeksInISOWeekYear=function(){return P(this.isoWeekYear(),1,4)},i.date=ve,i.day=i.days=function(e){if(!this.isValid())return null!=e?this:NaN;var t,n,s=this._isUTC?this._d.getUTCDay():this._d.getDay();return null!=e?(t=e,n=this.localeData(),e="string"!=typeof t?t:isNaN(t)?"number"==typeof(t=n.weekdaysParse(t))?t:null:parseInt(t,10),this.add(e-s,"d")):s},i.weekday=function(e){if(!this.isValid())return null!=e?this:NaN;var t=(this.day()+7-this.localeData()._week.dow)%7;return null==e?t:this.add(e-t,"d")},i.isoWeekday=function(e){return this.isValid()?null!=e?(t=e,n=this.localeData(),n="string"==typeof t?n.weekdaysParse(t)%7||7:isNaN(t)?null:t,this.day(this.day()%7?n:n-7)):this.day()||7:null!=e?this:NaN;var t,n},i.dayOfYear=function(e){var t=Math.round((this.clone().startOf("day")-this.clone().startOf("year"))/864e5)+1;return null==e?t:this.add(e-t,"d")},i.hour=i.hours=v,i.minute=i.minutes=_e,i.second=i.seconds=ke,i.millisecond=i.milliseconds=ye,i.utcOffset=function(e,t,n){var s,i=this._offset||0;if(!this.isValid())return null!=e?this:NaN;if(null==e)return this._isUTC?i:Et(this);if("string"==typeof e){if(null===(e=Vt(Ye,e)))return this}else Math.abs(e)<16&&!n&&(e*=60);return!this._isUTC&&t&&(s=Et(this)),this._offset=e,this._isUTC=!0,null!=s&&this.add(s,"m"),i!==e&&(!t||this._changeInProgress?qt(this,C(e-i,"m"),1,!1):this._changeInProgress||(this._changeInProgress=!0,f.updateOffset(this,!0),this._changeInProgress=null)),this},i.utc=function(e){return this.utcOffset(0,e)},i.local=function(e){return this._isUTC&&(this.utcOffset(0,e),this._isUTC=!1,e&&this.subtract(Et(this),"m")),this},i.parseZone=function(){var e;return null!=this._tzm?this.utcOffset(this._tzm,!1,!0):"string"==typeof this._i&&(null!=(e=Vt(Se,this._i))?this.utcOffset(e):this.utcOffset(0,!0)),this},i.hasAlignedHourOffset=function(e){return!!this.isValid()&&(e=e?W(e).utcOffset():0,(this.utcOffset()-e)%60==0)},i.isDST=function(){return this.utcOffset()>this.clone().month(0).utcOffset()||this.utcOffset()>this.clone().month(5).utcOffset()},i.isLocal=function(){return!!this.isValid()&&!this._isUTC},i.isUtcOffset=function(){return!!this.isValid()&&this._isUTC},i.isUtc=At,i.isUTC=At,i.zoneAbbr=function(){return this._isUTC?"UTC":""},i.zoneName=function(){return this._isUTC?"Coordinated Universal Time":""},i.dates=e("dates accessor is deprecated. Use date instead.",ve),i.months=e("months accessor is deprecated. Use month instead",Ge),i.years=e("years accessor is deprecated. Use year instead",Ie),i.zone=e("moment().zone is deprecated, use moment().utcOffset instead. http://momentjs.com/guides/#/warnings/zone/",function(e,t){return null!=e?(this.utcOffset(e="string"!=typeof e?-e:e,t),this):-this.utcOffset()}),i.isDSTShifted=e("isDSTShifted is deprecated. See http://momentjs.com/guides/#/warnings/dst-shifted/ for more information",function(){if(!o(this._isDSTShifted))return this._isDSTShifted;var e,t={};return $(t,this),(t=Nt(t))._a?(e=(t._isUTC?l:W)(t._a),this._isDSTShifted=this.isValid()&&0<function(e,t,n){for(var s=Math.min(e.length,t.length),i=Math.abs(e.length-t.length),r=0,a=0;a<s;a++)(n&&e[a]!==t[a]||!n&&g(e[a])!==g(t[a]))&&r++;return r+i}(t._a,e.toArray())):this._isDSTShifted=!1,this._isDSTShifted});w=K.prototype;function cn(e,t,n,s){var i=mt(),s=l().set(s,t);return i[n](s,e)}function fn(e,t,n){if(u(e)&&(t=e,e=void 0),e=e||"",null!=t)return cn(e,t,n,"month");for(var s=[],i=0;i<12;i++)s[i]=cn(e,i,n,"month");return s}function mn(e,t,n,s){t=("boolean"==typeof e?u(t)&&(n=t,t=void 0):(t=e,e=!1,u(n=t)&&(n=t,t=void 0)),t||"");var i,r=mt(),a=e?r._week.dow:0,o=[];if(null!=n)return cn(t,(n+a)%7,s,"day");for(i=0;i<7;i++)o[i]=cn(t,(i+a)%7,s,"day");return o}w.calendar=function(e,t,n){return d(e=this._calendar[e]||this._calendar.sameElse)?e.call(t,n):e},w.longDateFormat=function(e){var t=this._longDateFormat[e],n=this._longDateFormat[e.toUpperCase()];return t||!n?t:(this._longDateFormat[e]=n.match(te).map(function(e){return"MMMM"===e||"MM"===e||"DD"===e||"dddd"===e?e.slice(1):e}).join(""),this._longDateFormat[e])},w.invalidDate=function(){return this._invalidDate},w.ordinal=function(e){return this._ordinal.replace("%d",e)},w.preparse=dn,w.postformat=dn,w.relativeTime=function(e,t,n,s){var i=this._relativeTime[n];return d(i)?i(e,t,n,s):i.replace(/%d/i,e)},w.pastFuture=function(e,t){return d(e=this._relativeTime[0<e?"future":"past"])?e(t):e.replace(/%s/i,t)},w.set=function(e){var t,n;for(n in e)c(e,n)&&(d(t=e[n])?this[n]=t:this["_"+n]=t);this._config=e,this._dayOfMonthOrdinalParseLenient=new RegExp((this._dayOfMonthOrdinalParse.source||this._ordinalParse.source)+"|"+/\d{1,2}/.source)},w.eras=function(e,t){for(var n,s=this._eras||mt("en")._eras,i=0,r=s.length;i<r;++i)switch("string"==typeof s[i].since&&(n=f(s[i].since).startOf("day"),s[i].since=n.valueOf()),typeof s[i].until){case"undefined":s[i].until=1/0;break;case"string":n=f(s[i].until).startOf("day").valueOf(),s[i].until=n.valueOf()}return s},w.erasParse=function(e,t,n){var s,i,r,a,o,u=this.eras();for(e=e.toUpperCase(),s=0,i=u.length;s<i;++s)if(r=u[s].name.toUpperCase(),a=u[s].abbr.toUpperCase(),o=u[s].narrow.toUpperCase(),n)switch(t){case"N":case"NN":case"NNN":if(a===e)return u[s];break;case"NNNN":if(r===e)return u[s];break;case"NNNNN":if(o===e)return u[s]}else if(0<=[r,a,o].indexOf(e))return u[s]},w.erasConvertYear=function(e,t){var n=e.since<=e.until?1:-1;return void 0===t?f(e.since).year():f(e.since).year()+(t-e.offset)*n},w.erasAbbrRegex=function(e){return c(this,"_erasAbbrRegex")||an.call(this),e?this._erasAbbrRegex:this._erasRegex},w.erasNameRegex=function(e){return c(this,"_erasNameRegex")||an.call(this),e?this._erasNameRegex:this._erasRegex},w.erasNarrowRegex=function(e){return c(this,"_erasNarrowRegex")||an.call(this),e?this._erasNarrowRegex:this._erasRegex},w.months=function(e,t){return e?(a(this._months)?this._months:this._months[(this._months.isFormat||He).test(t)?"format":"standalone"])[e.month()]:a(this._months)?this._months:this._months.standalone},w.monthsShort=function(e,t){return e?(a(this._monthsShort)?this._monthsShort:this._monthsShort[He.test(t)?"format":"standalone"])[e.month()]:a(this._monthsShort)?this._monthsShort:this._monthsShort.standalone},w.monthsParse=function(e,t,n){var s,i;if(this._monthsParseExact)return function(e,t,n){var s,i,r,e=e.toLocaleLowerCase();if(!this._monthsParse)for(this._monthsParse=[],this._longMonthsParse=[],this._shortMonthsParse=[],s=0;s<12;++s)r=l([2e3,s]),this._shortMonthsParse[s]=this.monthsShort(r,"").toLocaleLowerCase(),this._longMonthsParse[s]=this.months(r,"").toLocaleLowerCase();return n?"MMM"===t?-1!==(i=S.call(this._shortMonthsParse,e))?i:null:-1!==(i=S.call(this._longMonthsParse,e))?i:null:"MMM"===t?-1!==(i=S.call(this._shortMonthsParse,e))||-1!==(i=S.call(this._longMonthsParse,e))?i:null:-1!==(i=S.call(this._longMonthsParse,e))||-1!==(i=S.call(this._shortMonthsParse,e))?i:null}.call(this,e,t,n);for(this._monthsParse||(this._monthsParse=[],this._longMonthsParse=[],this._shortMonthsParse=[]),s=0;s<12;s++){if(i=l([2e3,s]),n&&!this._longMonthsParse[s]&&(this._longMonthsParse[s]=new RegExp("^"+this.months(i,"").replace(".","")+"$","i"),this._shortMonthsParse[s]=new RegExp("^"+this.monthsShort(i,"").replace(".","")+"$","i")),n||this._monthsParse[s]||(i="^"+this.months(i,"")+"|^"+this.monthsShort(i,""),this._monthsParse[s]=new RegExp(i.replace(".",""),"i")),n&&"MMMM"===t&&this._longMonthsParse[s].test(e))return s;if(n&&"MMM"===t&&this._shortMonthsParse[s].test(e))return s;if(!n&&this._monthsParse[s].test(e))return s}},w.monthsRegex=function(e){return this._monthsParseExact?(c(this,"_monthsRegex")||Ee.call(this),e?this._monthsStrictRegex:this._monthsRegex):(c(this,"_monthsRegex")||(this._monthsRegex=Le),this._monthsStrictRegex&&e?this._monthsStrictRegex:this._monthsRegex)},w.monthsShortRegex=function(e){return this._monthsParseExact?(c(this,"_monthsRegex")||Ee.call(this),e?this._monthsShortStrictRegex:this._monthsShortRegex):(c(this,"_monthsShortRegex")||(this._monthsShortRegex=Fe),this._monthsShortStrictRegex&&e?this._monthsShortStrictRegex:this._monthsShortRegex)},w.week=function(e){return qe(e,this._week.dow,this._week.doy).week},w.firstDayOfYear=function(){return this._week.doy},w.firstDayOfWeek=function(){return this._week.dow},w.weekdays=function(e,t){return t=a(this._weekdays)?this._weekdays:this._weekdays[e&&!0!==e&&this._weekdays.isFormat.test(t)?"format":"standalone"],!0===e?Be(t,this._week.dow):e?t[e.day()]:t},w.weekdaysMin=function(e){return!0===e?Be(this._weekdaysMin,this._week.dow):e?this._weekdaysMin[e.day()]:this._weekdaysMin},w.weekdaysShort=function(e){return!0===e?Be(this._weekdaysShort,this._week.dow):e?this._weekdaysShort[e.day()]:this._weekdaysShort},w.weekdaysParse=function(e,t,n){var s,i;if(this._weekdaysParseExact)return function(e,t,n){var s,i,r,e=e.toLocaleLowerCase();if(!this._weekdaysParse)for(this._weekdaysParse=[],this._shortWeekdaysParse=[],this._minWeekdaysParse=[],s=0;s<7;++s)r=l([2e3,1]).day(s),this._minWeekdaysParse[s]=this.weekdaysMin(r,"").toLocaleLowerCase(),this._shortWeekdaysParse[s]=this.weekdaysShort(r,"").toLocaleLowerCase(),this._weekdaysParse[s]=this.weekdays(r,"").toLocaleLowerCase();return n?"dddd"===t?-1!==(i=S.call(this._weekdaysParse,e))?i:null:"ddd"===t?-1!==(i=S.call(this._shortWeekdaysParse,e))?i:null:-1!==(i=S.call(this._minWeekdaysParse,e))?i:null:"dddd"===t?-1!==(i=S.call(this._weekdaysParse,e))||-1!==(i=S.call(this._shortWeekdaysParse,e))||-1!==(i=S.call(this._minWeekdaysParse,e))?i:null:"ddd"===t?-1!==(i=S.call(this._shortWeekdaysParse,e))||-1!==(i=S.call(this._weekdaysParse,e))||-1!==(i=S.call(this._minWeekdaysParse,e))?i:null:-1!==(i=S.call(this._minWeekdaysParse,e))||-1!==(i=S.call(this._weekdaysParse,e))||-1!==(i=S.call(this._shortWeekdaysParse,e))?i:null}.call(this,e,t,n);for(this._weekdaysParse||(this._weekdaysParse=[],this._minWeekdaysParse=[],this._shortWeekdaysParse=[],this._fullWeekdaysParse=[]),s=0;s<7;s++){if(i=l([2e3,1]).day(s),n&&!this._fullWeekdaysParse[s]&&(this._fullWeekdaysParse[s]=new RegExp("^"+this.weekdays(i,"").replace(".","\\.?")+"$","i"),this._shortWeekdaysParse[s]=new RegExp("^"+this.weekdaysShort(i,"").replace(".","\\.?")+"$","i"),this._minWeekdaysParse[s]=new RegExp("^"+this.weekdaysMin(i,"").replace(".","\\.?")+"$","i")),this._weekdaysParse[s]||(i="^"+this.weekdays(i,"")+"|^"+this.weekdaysShort(i,"")+"|^"+this.weekdaysMin(i,""),this._weekdaysParse[s]=new RegExp(i.replace(".",""),"i")),n&&"dddd"===t&&this._fullWeekdaysParse[s].test(e))return s;if(n&&"ddd"===t&&this._shortWeekdaysParse[s].test(e))return s;if(n&&"dd"===t&&this._minWeekdaysParse[s].test(e))return s;if(!n&&this._weekdaysParse[s].test(e))return s}},w.weekdaysRegex=function(e){return this._weekdaysParseExact?(c(this,"_weekdaysRegex")||nt.call(this),e?this._weekdaysStrictRegex:this._weekdaysRegex):(c(this,"_weekdaysRegex")||(this._weekdaysRegex=Ke),this._weekdaysStrictRegex&&e?this._weekdaysStrictRegex:this._weekdaysRegex)},w.weekdaysShortRegex=function(e){return this._weekdaysParseExact?(c(this,"_weekdaysRegex")||nt.call(this),e?this._weekdaysShortStrictRegex:this._weekdaysShortRegex):(c(this,"_weekdaysShortRegex")||(this._weekdaysShortRegex=et),this._weekdaysShortStrictRegex&&e?this._weekdaysShortStrictRegex:this._weekdaysShortRegex)},w.weekdaysMinRegex=function(e){return this._weekdaysParseExact?(c(this,"_weekdaysRegex")||nt.call(this),e?this._weekdaysMinStrictRegex:this._weekdaysMinRegex):(c(this,"_weekdaysMinRegex")||(this._weekdaysMinRegex=tt),this._weekdaysMinStrictRegex&&e?this._weekdaysMinStrictRegex:this._weekdaysMinRegex)},w.isPM=function(e){return"p"===(e+"").toLowerCase().charAt(0)},w.meridiem=function(e,t,n){return 11<e?n?"pm":"PM":n?"am":"AM"},ct("en",{eras:[{since:"0001-01-01",until:1/0,offset:1,name:"Anno Domini",narrow:"AD",abbr:"AD"},{since:"0000-12-31",until:-1/0,offset:1,name:"Before Christ",narrow:"BC",abbr:"BC"}],dayOfMonthOrdinalParse:/\d{1,2}(th|st|nd|rd)/,ordinal:function(e){var t=e%10;return e+(1===g(e%100/10)?"th":1==t?"st":2==t?"nd":3==t?"rd":"th")}}),f.lang=e("moment.lang is deprecated. Use moment.locale instead.",ct),f.langData=e("moment.langData is deprecated. Use moment.localeData instead.",mt);var _n=Math.abs;function yn(e,t,n,s){t=C(t,n);return e._milliseconds+=s*t._milliseconds,e._days+=s*t._days,e._months+=s*t._months,e._bubble()}function gn(e){return e<0?Math.floor(e):Math.ceil(e)}function wn(e){return 4800*e/146097}function pn(e){return 146097*e/4800}function vn(e){return function(){return this.as(e)}}pe=vn("ms"),me=vn("s"),Ce=vn("m"),we=vn("h"),ge=vn("d"),Je=vn("w"),v=vn("M"),_e=vn("Q"),ke=vn("y");function kn(e){return function(){return this.isValid()?this._data[e]:NaN}}var ye=kn("milliseconds"),ve=kn("seconds"),Ie=kn("minutes"),w=kn("hours"),Mn=kn("days"),Dn=kn("months"),Sn=kn("years");var Yn=Math.round,On={ss:44,s:45,m:45,h:22,d:26,w:null,M:11};function bn(e,t,n,s){var i=C(e).abs(),r=Yn(i.as("s")),a=Yn(i.as("m")),o=Yn(i.as("h")),u=Yn(i.as("d")),l=Yn(i.as("M")),h=Yn(i.as("w")),i=Yn(i.as("y")),r=(r<=n.ss?["s",r]:r<n.s&&["ss",r])||a<=1&&["m"]||a<n.m&&["mm",a]||o<=1&&["h"]||o<n.h&&["hh",o]||u<=1&&["d"]||u<n.d&&["dd",u];return(r=(r=null!=n.w?r||h<=1&&["w"]||h<n.w&&["ww",h]:r)||l<=1&&["M"]||l<n.M&&["MM",l]||i<=1&&["y"]||["yy",i])[2]=t,r[3]=0<+e,r[4]=s,function(e,t,n,s,i){return i.relativeTime(t||1,!!n,e,s)}.apply(null,r)}var xn=Math.abs;function Tn(e){return(0<e)-(e<0)||+e}function Nn(){if(!this.isValid())return this.localeData().invalidDate();var e,t,n,s,i,r,a,o=xn(this._milliseconds)/1e3,u=xn(this._days),l=xn(this._months),h=this.asSeconds();return h?(e=y(o/60),t=y(e/60),o%=60,e%=60,n=y(l/12),l%=12,s=o?o.toFixed(3).replace(/\.?0+$/,""):"",i=Tn(this._months)!==Tn(h)?"-":"",r=Tn(this._days)!==Tn(h)?"-":"",a=Tn(this._milliseconds)!==Tn(h)?"-":"",(h<0?"-":"")+"P"+(n?i+n+"Y":"")+(l?i+l+"M":"")+(u?r+u+"D":"")+(t||e||o?"T":"")+(t?a+t+"H":"")+(e?a+e+"M":"")+(o?a+s+"S":"")):"P0D"}var U=Ct.prototype;return U.isValid=function(){return this._isValid},U.abs=function(){var e=this._data;return this._milliseconds=_n(this._milliseconds),this._days=_n(this._days),this._months=_n(this._months),e.milliseconds=_n(e.milliseconds),e.seconds=_n(e.seconds),e.minutes=_n(e.minutes),e.hours=_n(e.hours),e.months=_n(e.months),e.years=_n(e.years),this},U.add=function(e,t){return yn(this,e,t,1)},U.subtract=function(e,t){return yn(this,e,t,-1)},U.as=function(e){if(!this.isValid())return NaN;var t,n,s=this._milliseconds;if("month"===(e=_(e))||"quarter"===e||"year"===e)switch(t=this._days+s/864e5,n=this._months+wn(t),e){case"month":return n;case"quarter":return n/3;case"year":return n/12}else switch(t=this._days+Math.round(pn(this._months)),e){case"week":return t/7+s/6048e5;case"day":return t+s/864e5;case"hour":return 24*t+s/36e5;case"minute":return 1440*t+s/6e4;case"second":return 86400*t+s/1e3;case"millisecond":return Math.floor(864e5*t)+s;default:throw new Error("Unknown unit "+e)}},U.asMilliseconds=pe,U.asSeconds=me,U.asMinutes=Ce,U.asHours=we,U.asDays=ge,U.asWeeks=Je,U.asMonths=v,U.asQuarters=_e,U.asYears=ke,U.valueOf=function(){return this.isValid()?this._milliseconds+864e5*this._days+this._months%12*2592e6+31536e6*g(this._months/12):NaN},U._bubble=function(){var e=this._milliseconds,t=this._days,n=this._months,s=this._data;return 0<=e&&0<=t&&0<=n||e<=0&&t<=0&&n<=0||(e+=864e5*gn(pn(n)+t),n=t=0),s.milliseconds=e%1e3,e=y(e/1e3),s.seconds=e%60,e=y(e/60),s.minutes=e%60,e=y(e/60),s.hours=e%24,t+=y(e/24),n+=e=y(wn(t)),t-=gn(pn(e)),e=y(n/12),n%=12,s.days=t,s.months=n,s.years=e,this},U.clone=function(){return C(this)},U.get=function(e){return e=_(e),this.isValid()?this[e+"s"]():NaN},U.milliseconds=ye,U.seconds=ve,U.minutes=Ie,U.hours=w,U.days=Mn,U.weeks=function(){return y(this.days()/7)},U.months=Dn,U.years=Sn,U.humanize=function(e,t){if(!this.isValid())return this.localeData().invalidDate();var n=!1,s=On;return"object"==typeof e&&(t=e,e=!1),"boolean"==typeof e&&(n=e),"object"==typeof t&&(s=Object.assign({},On,t),null!=t.s&&null==t.ss&&(s.ss=t.s-1)),e=this.localeData(),t=bn(this,!n,s,e),n&&(t=e.pastFuture(+this,t)),e.postformat(t)},U.toISOString=Nn,U.toString=Nn,U.toJSON=Nn,U.locale=Xt,U.localeData=Kt,U.toIsoString=e("toIsoString() is deprecated. Please use toISOString() instead (notice the capitals)",Nn),U.lang=Xe,s("X",0,0,"unix"),s("x",0,0,"valueOf"),k("x",De),k("X",/[+-]?\d+(\.\d{1,3})?/),D("X",function(e,t,n){n._d=new Date(1e3*parseFloat(e))}),D("x",function(e,t,n){n._d=new Date(g(e))}),f.version="2.29.4",H=W,f.fn=i,f.min=function(){return Rt("isBefore",[].slice.call(arguments,0))},f.max=function(){return Rt("isAfter",[].slice.call(arguments,0))},f.now=function(){return Date.now?Date.now():+new Date},f.utc=l,f.unix=function(e){return W(1e3*e)},f.months=function(e,t){return fn(e,t,"months")},f.isDate=V,f.locale=ct,f.invalid=I,f.duration=C,f.isMoment=h,f.weekdays=function(e,t,n){return mn(e,t,n,"weekdays")},f.parseZone=function(){return W.apply(null,arguments).parseZone()},f.localeData=mt,f.isDuration=Ut,f.monthsShort=function(e,t){return fn(e,t,"monthsShort")},f.weekdaysMin=function(e,t,n){return mn(e,t,n,"weekdaysMin")},f.defineLocale=ft,f.updateLocale=function(e,t){var n,s;return null!=t?(s=ot,null!=R[e]&&null!=R[e].parentLocale?R[e].set(X(R[e]._config,t)):(t=X(s=null!=(n=dt(e))?n._config:s,t),null==n&&(t.abbr=e),(s=new K(t)).parentLocale=R[e],R[e]=s),ct(e)):null!=R[e]&&(null!=R[e].parentLocale?(R[e]=R[e].parentLocale,e===ct()&&ct(e)):null!=R[e]&&delete R[e]),R[e]},f.locales=function(){return ee(R)},f.weekdaysShort=function(e,t,n){return mn(e,t,n,"weekdaysShort")},f.normalizeUnits=_,f.relativeTimeRounding=function(e){return void 0===e?Yn:"function"==typeof e&&(Yn=e,!0)},f.relativeTimeThreshold=function(e,t){return void 0!==On[e]&&(void 0===t?On[e]:(On[e]=t,"s"===e&&(On.ss=t-1),!0))},f.calendarFormat=function(e,t){return(e=e.diff(t,"days",!0))<-6?"sameElse":e<-1?"lastWeek":e<0?"lastDay":e<1?"sameDay":e<2?"nextDay":e<7?"nextWeek":"sameElse"},f.prototype=i,f.HTML5_FMT={DATETIME_LOCAL:"YYYY-MM-DDTHH:mm",DATETIME_LOCAL_SECONDS:"YYYY-MM-DDTHH:mm:ss",DATETIME_LOCAL_MS:"YYYY-MM-DDTHH:mm:ss.SSS",DATE:"YYYY-MM-DD",TIME:"HH:mm",TIME_SECONDS:"HH:mm:ss",TIME_MS:"HH:mm:ss.SSS",WEEK:"GGGG-[W]WW",MONTH:"YYYY-MM"},f});;
// version 1.6.0
// http://welcome.totheinter.net/columnizer-jquery-plugin/
// created by: Adam Wulf @adamwulf, adam.wulf@gmail.com

(function($){

 $.fn.columnize = function(options) {


	var defaults = {
		// default width of columns
		width: 400,
		// optional # of columns instead of width
		columns : false,
		// true to build columns once regardless of window resize
		// false to rebuild when content box changes bounds
		buildOnce : false,
		// an object with options if the text should overflow
		// it's container if it can't fit within a specified height
		overflow : false,
		// this function is called after content is columnized
		doneFunc : function(){},
		// if the content should be columnized into a 
		// container node other than it's own node
		target : false,
		// re-columnizing when images reload might make things
		// run slow. so flip this to true if it's causing delays
		ignoreImageLoading : true,
		// should columns float left or right
		columnFloat : "left",
		// ensure the last column is never the tallest column
		lastNeverTallest : false,
		// (int) the minimum number of characters to jump when splitting
		// text nodes. smaller numbers will result in higher accuracy
		// column widths, but will take slightly longer
		accuracy : false,
		// don't automatically layout columns, only use manual columnbreak
		manualBreaks : false,
		// previx for all the CSS classes used by this plugin
		// default to empty string for backwards compatibility
		cssClassPrefix : ""
	};
	options = $.extend(defaults, options);

	if(typeof(options.width) == "string"){
		options.width = parseInt(options.width,10);
		if(isNaN(options.width)){
			options.width = defaults.width;
		}
	}

    return this.each(function() {
		var $inBox = options.target ? $(options.target) : $(this);
		var maxHeight = $(this).height();
		var $cache = $('<div></div>'); // this is where we'll put the real content
		var lastWidth = 0;
		var columnizing = false;
		var manualBreaks = options.manualBreaks;
		var cssClassPrefix = defaults.cssClassPrefix;
		if(typeof(options.cssClassPrefix) == "string"){
			cssClassPrefix = options.cssClassPrefix;
		}


		var adjustment = 0;

		$cache.append($(this).contents().clone(true));

		// images loading after dom load
		// can screw up the column heights,
		// so recolumnize after images load
		if(!options.ignoreImageLoading && !options.target){
			if(!$inBox.data("imageLoaded")){
				$inBox.data("imageLoaded", true);
				if($(this).find("img").length > 0){
					// only bother if there are
					// actually images...
					var func = function($inBox,$cache){ return function(){
							if(!$inBox.data("firstImageLoaded")){
								$inBox.data("firstImageLoaded", "true");
								$inBox.empty().append($cache.children().clone(true));
								$inBox.columnize(options);
							}
						};
					}($(this), $cache);
					$(this).find("img").one("load", func);
					$(this).find("img").one("abort", func);
					return;
				}
			}
		}

		$inBox.empty();

		columnizeIt();

		if(!options.buildOnce){
			$(window).resize(function() {
				if(!options.buildOnce){
					if($inBox.data("timeout")){
						clearTimeout($inBox.data("timeout"));
					}
					$inBox.data("timeout", setTimeout(columnizeIt, 200));
				}
			});
		}

		function prefixTheClassName(className, withDot){
			var dot = withDot ? "." : "";
			if(cssClassPrefix.length){
				return dot + cssClassPrefix + "-" + className;
			}
			return dot + className;
		}

		/**
		 * this fuction builds as much of a column as it can without
		 * splitting nodes in half. If the last node in the new column
		 * is a text node, then it will try to split that text node. otherwise
		 * it will leave the node in $pullOutHere and return with a height
		 * smaller than targetHeight.
		 * 
         * Returns a boolean on whether we did some splitting successfully at a text point
         * (so we know we don't need to split a real element). return false if the caller should
         * split a node if possible to end this column.
		 *
		 * @param putInHere, the jquery node to put elements into for the current column
		 * @param $pullOutHere, the jquery node to pull elements out of (uncolumnized html)
		 * @param $parentColumn, the jquery node for the currently column that's being added to
		 * @param targetHeight, the ideal height for the column, get as close as we can to this height
		 */
		function columnize($putInHere, $pullOutHere, $parentColumn, targetHeight){
			//
			// add as many nodes to the column as we can,
			// but stop once our height is too tall
			while((manualBreaks || $parentColumn.height() < targetHeight) &&
				$pullOutHere[0].childNodes.length){
				var node = $pullOutHere[0].childNodes[0];
				//
				// Because we're not cloning, jquery will actually move the element"
				// http://welcome.totheinter.net/2009/03/19/the-undocumented-life-of-jquerys-append/
				if($(node).find(prefixTheClassName("columnbreak", true)).length){
					//
					// our column is on a column break, so just end here
					return;
				}
				if($(node).hasClass(prefixTheClassName("columnbreak"))){
					//
					// our column is on a column break, so just end here
					return;
				}
				$putInHere.append(node);
			}
			if($putInHere[0].childNodes.length === 0) return;

			// now we're too tall, so undo the last one
			var kids = $putInHere[0].childNodes;
			var lastKid = kids[kids.length-1];
			$putInHere[0].removeChild(lastKid);
			var $item = $(lastKid);

			// now lets try to split that last node
			// to fit as much of it as we can into this column
			if($item[0].nodeType == 3){
				// it's a text node, split it up
				var oText = $item[0].nodeValue;
				var counter2 = options.width / 18;
				if(options.accuracy)
				counter2 = options.accuracy;
				var columnText;
				var latestTextNode = null;
				while($parentColumn.height() < targetHeight && oText.length){
					var indexOfSpace = oText.indexOf(' ', counter2);
					if (indexOfSpace != -1) {
						columnText = oText.substring(0, oText.indexOf(' ', counter2));
					} else {
						columnText = oText;
					}
					latestTextNode = document.createTextNode(columnText);
					$putInHere.append(latestTextNode);

					if(oText.length > counter2 && indexOfSpace != -1){
						oText = oText.substring(indexOfSpace);
					}else{
						oText = "";
					}
				}
				if($parentColumn.height() >= targetHeight && latestTextNode !== null){
					// too tall :(
					$putInHere[0].removeChild(latestTextNode);
					oText = latestTextNode.nodeValue + oText;
				}
				if(oText.length){
					$item[0].nodeValue = oText;
				}else{
					return false; // we ate the whole text node, move on to the next node
				}
			}

			if($pullOutHere.contents().length){
				$pullOutHere.prepend($item);
			}else{
				$pullOutHere.append($item);
			}

			return $item[0].nodeType == 3;
		}

		/**
		 * Split up an element, which is more complex than splitting text. We need to create 
		 * two copies of the element with it's contents divided between each
		 */
		function split($putInHere, $pullOutHere, $parentColumn, targetHeight){
			if($putInHere.contents(":last").find(prefixTheClassName("columnbreak", true)).length){
				//
				// our column is on a column break, so just end here
				return;
			}
			if($putInHere.contents(":last").hasClass(prefixTheClassName("columnbreak"))){
				//
				// our column is on a column break, so just end here
				return;
			}
			if($pullOutHere.contents().length){
				var $cloneMe = $pullOutHere.contents(":first");
				//
				// make sure we're splitting an element
				if($cloneMe.get(0).nodeType != 1) return;

				//
				// clone the node with all data and events
				var $clone = $cloneMe.clone(true);
				//
				// need to support both .prop and .attr if .prop doesn't exist.
				// this is for backwards compatibility with older versions of jquery.
				if($cloneMe.hasClass(prefixTheClassName("columnbreak"))){
					//
					// ok, we have a columnbreak, so add it into
					// the column and exit
					$putInHere.append($clone);
					$cloneMe.remove();
				}else if (manualBreaks){
					// keep adding until we hit a manual break
					$putInHere.append($clone);
					$cloneMe.remove();
				}else if($clone.get(0).nodeType == 1 && !$clone.hasClass(prefixTheClassName("dontend"))){
					$putInHere.append($clone);
					if($clone.is("img") && $parentColumn.height() < targetHeight + 20){
						//
						// we can't split an img in half, so just add it
						// to the column and remove it from the pullOutHere section
						$cloneMe.remove();
					}else if(!$cloneMe.hasClass(prefixTheClassName("dontsplit")) && $parentColumn.height() < targetHeight + 20){
						//
						// pretty close fit, and we're not allowed to split it, so just
						// add it to the column, remove from pullOutHere, and be done
						$cloneMe.remove();
					}else if($clone.is("img") || $cloneMe.hasClass(prefixTheClassName("dontsplit"))){
						//
						// it's either an image that's too tall, or an unsplittable node
						// that's too tall. leave it in the pullOutHere and we'll add it to the 
						// next column
						$clone.remove();
					}else{
						//
						// ok, we're allowed to split the node in half, so empty out
						// the node in the column we're building, and start splitting
						// it in half, leaving some of it in pullOutHere
						$clone.empty();
						if(!columnize($clone, $cloneMe, $parentColumn, targetHeight)){
							// this node still has non-text nodes to split
							// add the split class and then recur
							$cloneMe.addClass(prefixTheClassName("split"));
							if($cloneMe.children().length){
								split($clone, $cloneMe, $parentColumn, targetHeight);
							}
						}else{
							// this node only has text node children left, add the
							// split class and move on.
							$cloneMe.addClass(prefixTheClassName("split"));
						}
						if($clone.get(0).childNodes.length === 0){
							// it was split, but nothing is in it :(
							$clone.remove();
						}
					}
				}
			}
		}


		function singleColumnizeIt() {
			if ($inBox.data("columnized") && $inBox.children().length == 1) {
				return;
			}
			$inBox.data("columnized", true);
			$inBox.data("columnizing", true);

			$inBox.empty();
			$inBox.append($("<div class='"
				+ prefixTheClassName("first") + " "
				+ prefixTheClassName("last") + " "
				+ prefixTheClassName("column") + " "
				+ "' style='width:100%; float: " + options.columnFloat + ";'></div>")); //"
			$col = $inBox.children().eq($inBox.children().length-1);
			$destroyable = $cache.clone(true);
			if(options.overflow){
				targetHeight = options.overflow.height;
				columnize($col, $destroyable, $col, targetHeight);
				// make sure that the last item in the column isn't a "dontend"
				if(!$destroyable.contents().find(":first-child").hasClass(prefixTheClassName("dontend"))){
					split($col, $destroyable, $col, targetHeight);
				}

				while($col.contents(":last").length && checkDontEndColumn($col.contents(":last").get(0))){
					var $lastKid = $col.contents(":last");
					$lastKid.remove();
					$destroyable.prepend($lastKid);
				}

				var html = "";
				var div = document.createElement('DIV');
				while($destroyable[0].childNodes.length > 0){
					var kid = $destroyable[0].childNodes[0];
					if(kid.attributes){
						for(var i=0;i<kid.attributes.length;i++){
							if(kid.attributes[i].nodeName.indexOf("jQuery") === 0){
								kid.removeAttribute(kid.attributes[i].nodeName);
							}
						}
					}
					div.innerHTML = "";
					div.appendChild($destroyable[0].childNodes[0]);
					html += div.innerHTML;
				}
				var overflow = $(options.overflow.id)[0];
				overflow.innerHTML = html;

			}else{
				$col.append($destroyable);
			}
			$inBox.data("columnizing", false);

			if(options.overflow && options.overflow.doneFunc){
				options.overflow.doneFunc();
			}

		}

		/**
		 * returns true if the input dom node
		 * should not end a column.
		 * returns false otherwise
		 */
		function checkDontEndColumn(dom){
			if(dom.nodeType == 3){
				// text node. ensure that the text
				// is not 100% whitespace
				if(/^\s+$/.test(dom.nodeValue)){
						//
						// ok, it's 100% whitespace,
						// so we should return checkDontEndColumn
						// of the inputs previousSibling
						if(!dom.previousSibling) return false;
					return checkDontEndColumn(dom.previousSibling);
				}
				return false;
			}
			if(dom.nodeType != 1) return false;
			if($(dom).hasClass(prefixTheClassName("dontend"))) return true;
			if(dom.childNodes.length === 0) return false;
			return checkDontEndColumn(dom.childNodes[dom.childNodes.length-1]);
		}

		function columnizeIt() {
			//reset adjustment var
			adjustment = 0;
			if(lastWidth == $inBox.width()) return;
			lastWidth = $inBox.width();

			var numCols = Math.round($inBox.width() / options.width);
			var optionWidth = options.width;
			var optionHeight = options.height;
			if(options.columns) numCols = options.columns;
			if(manualBreaks){
				numCols = $cache.find(prefixTheClassName("columnbreak", true)).length + 1;
				optionWidth = false;
			}

//			if ($inBox.data("columnized") && numCols == $inBox.children().length) {
//				return;
//			}
			if(numCols <= 1){
				return singleColumnizeIt();
			}
			if($inBox.data("columnizing")) return;
			$inBox.data("columnized", true);
			$inBox.data("columnizing", true);

			$inBox.empty();
			$inBox.append($("<div style='width:" + (Math.floor(100 / numCols))+ "%; float: " + options.columnFloat + ";'></div>")); //"
			$col = $inBox.children(":last");
			$col.append($cache.clone());
			maxHeight = $col.height();
			$inBox.empty();

			var targetHeight = maxHeight / numCols;
			var firstTime = true;
			var maxLoops = 3;
			var scrollHorizontally = false;
			if(options.overflow){
				maxLoops = 1;
				targetHeight = options.overflow.height;
			}else if(optionHeight && optionWidth){
				maxLoops = 1;
				targetHeight = optionHeight;
				scrollHorizontally = true;
			}

			//
			// We loop as we try and workout a good height to use. We know it initially as an average 
			// but if the last column is higher than the first ones (which can happen, depending on split
			// points) we need to raise 'adjustment'. We try this over a few iterations until we're 'solid'.
			//
			// also, lets hard code the max loops to 20. that's /a lot/ of loops for columnizer,
			// and should keep run aways in check. if somehow someone has content combined with
			// options that would cause an infinite loop, then this'll definitely stop it.
			for(var loopCount=0;loopCount<maxLoops && loopCount<20;loopCount++){
				$inBox.empty();
				var $destroyable, className, $col, $lastKid;
				try{
					$destroyable = $cache.clone(true);
				}catch(e){
					// jquery in ie6 can't clone with true
					$destroyable = $cache.clone();
				}
				$destroyable.css("visibility", "hidden");
				// create the columns
				for (var i = 0; i < numCols; i++) {
					/* create column */
					className = (i === 0) ? prefixTheClassName("first") : "";
					className += " " + prefixTheClassName("column");
					className = (i == numCols - 1) ? (prefixTheClassName("last") + " " + className) : className;
					$inBox.append($("<div class='" + className + "' style='width:" + (Math.floor(100 / numCols))+ "%; float: " + options.columnFloat + ";'></div>")); //"
				}

				// fill all but the last column (unless overflowing)
				i = 0;
				while(i < numCols - (options.overflow ? 0 : 1) || scrollHorizontally && $destroyable.contents().length){
					if($inBox.children().length <= i){
						// we ran out of columns, make another
						$inBox.append($("<div class='" + className + "' style='width:" + (Math.floor(100 / numCols))+ "%; float: " + options.columnFloat + ";'></div>")); //"
					}
					$col = $inBox.children().eq(i);
					if(scrollHorizontally){
						$col.width(optionWidth + "px");
					}
					columnize($col, $destroyable, $col, targetHeight);
					// make sure that the last item in the column isn't a "dontend"
					split($col, $destroyable, $col, targetHeight);

					while($col.contents(":last").length && checkDontEndColumn($col.contents(":last").get(0))){
						$lastKid = $col.contents(":last");
						$lastKid.remove();
						$destroyable.prepend($lastKid);
					}
					i++;

					//
					// https://github.com/adamwulf/Columnizer-jQuery-Plugin/issues/47
					//
					// check for infinite loop.
					//
					// this could happen when a dontsplit or dontend item is taller than the column
					// we're trying to build, and its never actually added to a column.
					//
					// this results in empty columns being added with the dontsplit item
					// perpetually waiting to get put into a column. lets force the issue here
					if($col.contents().length === 0 && $destroyable.contents().length){
						//
						// ok, we're building zero content columns. this'll happen forever
						// since nothing can ever get taken out of destroyable.
						//
						// to fix, lets put 1 item from destroyable into the empty column
						// before we iterate
						$col.append($destroyable.contents(":first"));
					}else if(i == numCols - (options.overflow ? 0 : 1) && !options.overflow){
						//
						// ok, we're about to exit the while loop because we're done with all
						// columns except the last column.
						//
						// if $destroyable still has columnbreak nodes in it, then we need to keep
						// looping and creating more columns.
						if($destroyable.find(prefixTheClassName("columnbreak", true)).length){
							numCols ++;
						}
					}
				}
				if(options.overflow && !scrollHorizontally){
					var IE6 = false /*@cc_on || @_jscript_version < 5.7 @*/;
					var IE7 = (document.all) && (navigator.appVersion.indexOf("MSIE 7.") != -1);
					if(IE6 || IE7){
						var html = "";
						var div = document.createElement('DIV');
						while($destroyable[0].childNodes.length > 0){
							var kid = $destroyable[0].childNodes[0];
							for(i=0;i<kid.attributes.length;i++){
								if(kid.attributes[i].nodeName.indexOf("jQuery") === 0){
									kid.removeAttribute(kid.attributes[i].nodeName);
								}
							}
							div.innerHTML = "";
							div.appendChild($destroyable[0].childNodes[0]);
							html += div.innerHTML;
						}
						var overflow = $(options.overflow.id)[0];
						overflow.innerHTML = html;
					}else{
						$(options.overflow.id).empty().append($destroyable.contents().clone(true));
					}
				}else if(!scrollHorizontally){
					// the last column in the series
					$col = $inBox.children().eq($inBox.children().length-1);
					$destroyable.contents().each( function() {
						$col.append( $(this) );
					});
					var afterH = $col.height();
					var diff = afterH - targetHeight;
					var totalH = 0;
					var min = 10000000;
					var max = 0;
					var lastIsMax = false;
					var numberOfColumnsThatDontEndInAColumnBreak = 0;
					$inBox.children().each(function($inBox){ return function($item){
						var $col = $inBox.children().eq($item);
						var endsInBreak = $col.children(":last").find(prefixTheClassName("columnbreak", true)).length;
						if(!endsInBreak){
							var h = $col.height();
							lastIsMax = false;
							totalH += h;
							if(h > max) {
								max = h;
								lastIsMax = true;
							}
							if(h < min) min = h;
							numberOfColumnsThatDontEndInAColumnBreak++;
						}
					};
				}($inBox));

					var avgH = totalH / numberOfColumnsThatDontEndInAColumnBreak;
					if(totalH === 0){
						//
						// all columns end in a column break,
						// so we're done here
						loopCount = maxLoops;
					}else if(options.lastNeverTallest && lastIsMax){
						// the last column is the tallest
						// so allow columns to be taller
						// and retry
						//
						// hopefully this'll mean more content fits into
						// earlier columns, so that the last column
						// can be shorter than the rest
						adjustment += 30;

						targetHeight = targetHeight + 30;
						if(loopCount == maxLoops-1) maxLoops++;
					}else if(max - min > 30){
						// too much variation, try again
						targetHeight = avgH + 30;
					}else if(Math.abs(avgH-targetHeight) > 20){
						// too much variation, try again
						targetHeight = avgH;
					}else {
						// solid, we're done
						loopCount = maxLoops;
					}
				}else{
					// it's scrolling horizontally, fix the width/classes of the columns
					$inBox.children().each(function(i){
						$col = $inBox.children().eq(i);
						$col.width(optionWidth + "px");
						if(i === 0){
							$col.addClass(prefixTheClassName("first"));
						}else if(i==$inBox.children().length-1){
							$col.addClass(prefixTheClassName("last"));
						}else{
							$col.removeClass(prefixTheClassName("first"));
							$col.removeClass(prefixTheClassName("last"));
						}
					});
					$inBox.width($inBox.children().length * optionWidth + "px");
				}
				$inBox.append($("<br style='clear:both;'>"));
			}
			$inBox.find(prefixTheClassName("column", true)).find(":first" + prefixTheClassName("removeiffirst", true)).remove();
			$inBox.find(prefixTheClassName("column", true)).find(':last' + prefixTheClassName("removeiflast", true)).remove();
			$inBox.data("columnizing", false);

			if(options.overflow){
				options.overflow.doneFunc();
			}
			options.doneFunc();
		}
    });
 };
})(jQuery);
;
/*! Video.js v4.11.2 Copyright 2014 Brightcove, Inc. https://github.com/videojs/video.js/blob/master/LICENSE */ 
(function() {var b=void 0,f=!0,k=null,l=!1;function m(){return function(){}}function n(a){return function(){return this[a]}}function r(a){return function(){return a}}var s;document.createElement("video");document.createElement("audio");document.createElement("track");function t(a,c,d){if("string"===typeof a){0===a.indexOf("#")&&(a=a.slice(1));if(t.Fa[a])return t.Fa[a];a=t.w(a)}if(!a||!a.nodeName)throw new TypeError("The element or ID supplied is not valid. (videojs)");return a.player||new t.Player(a,c,d)}
var videojs=window.videojs=t;t.Yb="4.11";t.ed="https:"==document.location.protocol?"https://":"http://";
t.options={techOrder:["html5","flash"],html5:{},flash:{},width:300,height:150,defaultVolume:0,playbackRates:[],inactivityTimeout:2E3,children:{mediaLoader:{},posterImage:{},textTrackDisplay:{},loadingSpinner:{},bigPlayButton:{},controlBar:{},errorDisplay:{}},language:document.getElementsByTagName("html")[0].getAttribute("lang")||navigator.languages&&navigator.languages[0]||navigator.Me||navigator.language||"en",languages:{},notSupportedMessage:"No compatible source was found for this video."};
"GENERATED_CDN_VSN"!==t.Yb&&(videojs.options.flash.swf=t.ed+"vjs.zencdn.net/"+t.Yb+"/video-js.swf");t.sd=function(a,c){t.options.languages[a]=t.options.languages[a]!==b?t.Z.Ea(t.options.languages[a],c):c;return t.options.languages};t.Fa={};"function"===typeof define&&define.amd?define([],function(){return videojs}):"object"===typeof exports&&"object"===typeof module&&(module.exports=videojs);t.ua=t.CoreObject=m();
t.ua.extend=function(a){var c,d;a=a||{};c=a.init||a.i||this.prototype.init||this.prototype.i||m();d=function(){c.apply(this,arguments)};d.prototype=t.h.create(this.prototype);d.prototype.constructor=d;d.extend=t.ua.extend;d.create=t.ua.create;for(var e in a)a.hasOwnProperty(e)&&(d.prototype[e]=a[e]);return d};t.ua.create=function(){var a=t.h.create(this.prototype);this.apply(a,arguments);return a};
t.c=function(a,c,d){if(t.h.isArray(c))return u(t.c,a,c,d);var e=t.getData(a);e.C||(e.C={});e.C[c]||(e.C[c]=[]);d.p||(d.p=t.p++);e.C[c].push(d);e.W||(e.disabled=l,e.W=function(c){if(!e.disabled){c=t.zc(c);var d=e.C[c.type];if(d)for(var d=d.slice(0),j=0,p=d.length;j<p&&!c.Gc();j++)d[j].call(a,c)}});1==e.C[c].length&&(a.addEventListener?a.addEventListener(c,e.W,l):a.attachEvent&&a.attachEvent("on"+c,e.W))};
t.k=function(a,c,d){if(t.Bc(a)){var e=t.getData(a);if(e.C){if(t.h.isArray(c))return u(t.k,a,c,d);if(c){var g=e.C[c];if(g){if(d){if(d.p)for(e=0;e<g.length;e++)g[e].p===d.p&&g.splice(e--,1)}else e.C[c]=[];t.pc(a,c)}}else for(g in e.C)c=g,e.C[c]=[],t.pc(a,c)}}};t.pc=function(a,c){var d=t.getData(a);0===d.C[c].length&&(delete d.C[c],a.removeEventListener?a.removeEventListener(c,d.W,l):a.detachEvent&&a.detachEvent("on"+c,d.W));t.Kb(d.C)&&(delete d.C,delete d.W,delete d.disabled);t.Kb(d)&&t.Pc(a)};
t.zc=function(a){function c(){return f}function d(){return l}if(!a||!a.Lb){var e=a||window.event;a={};for(var g in e)"layerX"!==g&&("layerY"!==g&&"keyLocation"!==g)&&("returnValue"==g&&e.preventDefault||(a[g]=e[g]));a.target||(a.target=a.srcElement||document);a.relatedTarget=a.fromElement===a.target?a.toElement:a.fromElement;a.preventDefault=function(){e.preventDefault&&e.preventDefault();a.returnValue=l;a.Nd=c;a.defaultPrevented=f};a.Nd=d;a.defaultPrevented=l;a.stopPropagation=function(){e.stopPropagation&&
e.stopPropagation();a.cancelBubble=f;a.Lb=c};a.Lb=d;a.stopImmediatePropagation=function(){e.stopImmediatePropagation&&e.stopImmediatePropagation();a.Gc=c;a.stopPropagation()};a.Gc=d;if(a.clientX!=k){g=document.documentElement;var h=document.body;a.pageX=a.clientX+(g&&g.scrollLeft||h&&h.scrollLeft||0)-(g&&g.clientLeft||h&&h.clientLeft||0);a.pageY=a.clientY+(g&&g.scrollTop||h&&h.scrollTop||0)-(g&&g.clientTop||h&&h.clientTop||0)}a.which=a.charCode||a.keyCode;a.button!=k&&(a.button=a.button&1?0:a.button&
4?1:a.button&2?2:0)}return a};t.l=function(a,c){var d=t.Bc(a)?t.getData(a):{},e=a.parentNode||a.ownerDocument;"string"===typeof c&&(c={type:c,target:a});c=t.zc(c);d.W&&d.W.call(a,c);if(e&&!c.Lb()&&c.bubbles!==l)t.l(e,c);else if(!e&&!c.defaultPrevented&&(d=t.getData(c.target),c.target[c.type])){d.disabled=f;if("function"===typeof c.target[c.type])c.target[c.type]();d.disabled=l}return!c.defaultPrevented};
t.Q=function(a,c,d){function e(){t.k(a,c,e);d.apply(this,arguments)}if(t.h.isArray(c))return u(t.Q,a,c,d);e.p=d.p=d.p||t.p++;t.c(a,c,e)};function u(a,c,d,e){t.mc.forEach(d,function(d){a(c,d,e)})}var v=Object.prototype.hasOwnProperty;t.e=function(a,c){var d;c=c||{};d=document.createElement(a||"div");t.h.X(c,function(a,c){-1!==a.indexOf("aria-")||"role"==a?d.setAttribute(a,c):d[a]=c});return d};t.ba=function(a){return a.charAt(0).toUpperCase()+a.slice(1)};t.h={};
t.h.create=Object.create||function(a){function c(){}c.prototype=a;return new c};t.h.X=function(a,c,d){for(var e in a)v.call(a,e)&&c.call(d||this,e,a[e])};t.h.z=function(a,c){if(!c)return a;for(var d in c)v.call(c,d)&&(a[d]=c[d]);return a};t.h.Ad=function(a,c){var d,e,g;a=t.h.copy(a);for(d in c)v.call(c,d)&&(e=a[d],g=c[d],a[d]=t.h.Ya(e)&&t.h.Ya(g)?t.h.Ad(e,g):c[d]);return a};t.h.copy=function(a){return t.h.z({},a)};
t.h.Ya=function(a){return!!a&&"object"===typeof a&&"[object Object]"===a.toString()&&a.constructor===Object};t.h.isArray=Array.isArray||function(a){return"[object Array]"===Object.prototype.toString.call(a)};t.Pd=function(a){return a!==a};t.bind=function(a,c,d){function e(){return c.apply(a,arguments)}c.p||(c.p=t.p++);e.p=d?d+"_"+c.p:c.p;return e};t.xa={};t.p=1;t.expando="vdata"+(new Date).getTime();t.getData=function(a){var c=a[t.expando];c||(c=a[t.expando]=t.p++,t.xa[c]={});return t.xa[c]};
t.Bc=function(a){a=a[t.expando];return!(!a||t.Kb(t.xa[a]))};t.Pc=function(a){var c=a[t.expando];if(c){delete t.xa[c];try{delete a[t.expando]}catch(d){a.removeAttribute?a.removeAttribute(t.expando):a[t.expando]=k}}};t.Kb=function(a){for(var c in a)if(a[c]!==k)return l;return f};t.Xa=function(a,c){return-1!==(" "+a.className+" ").indexOf(" "+c+" ")};t.n=function(a,c){t.Xa(a,c)||(a.className=""===a.className?c:a.className+" "+c)};
t.r=function(a,c){var d,e;if(t.Xa(a,c)){d=a.className.split(" ");for(e=d.length-1;0<=e;e--)d[e]===c&&d.splice(e,1);a.className=d.join(" ")}};t.A=t.e("video");t.N=navigator.userAgent;t.md=/iPhone/i.test(t.N);t.ld=/iPad/i.test(t.N);t.nd=/iPod/i.test(t.N);t.kd=t.md||t.ld||t.nd;var aa=t,x;var y=t.N.match(/OS (\d+)_/i);x=y&&y[1]?y[1]:b;aa.Ae=x;t.hd=/Android/i.test(t.N);var ba=t,z;var A=t.N.match(/Android (\d+)(?:\.(\d+))?(?:\.(\d+))*/i),B,C;
A?(B=A[1]&&parseFloat(A[1]),C=A[2]&&parseFloat(A[2]),z=B&&C?parseFloat(A[1]+"."+A[2]):B?B:k):z=k;ba.Xb=z;t.od=t.hd&&/webkit/i.test(t.N)&&2.3>t.Xb;t.jd=/Firefox/i.test(t.N);t.Be=/Chrome/i.test(t.N);t.ic=!!("ontouchstart"in window||window.gd&&document instanceof window.gd);t.fd="backgroundSize"in t.A.style;t.Sc=function(a,c){t.h.X(c,function(c,e){e===k||"undefined"===typeof e||e===l?a.removeAttribute(c):a.setAttribute(c,e===f?"":e)})};
t.Ca=function(a){var c,d,e,g;c={};if(a&&a.attributes&&0<a.attributes.length){d=a.attributes;for(var h=d.length-1;0<=h;h--){e=d[h].name;g=d[h].value;if("boolean"===typeof a[e]||-1!==",autoplay,controls,loop,muted,default,".indexOf(","+e+","))g=g!==k?f:l;c[e]=g}}return c};
t.He=function(a,c){var d="";document.defaultView&&document.defaultView.getComputedStyle?d=document.defaultView.getComputedStyle(a,"").getPropertyValue(c):a.currentStyle&&(d=a["client"+c.substr(0,1).toUpperCase()+c.substr(1)]+"px");return d};t.Jb=function(a,c){c.firstChild?c.insertBefore(a,c.firstChild):c.appendChild(a)};t.Sa={};t.w=function(a){0===a.indexOf("#")&&(a=a.slice(1));return document.getElementById(a)};
t.Ba=function(a,c){c=c||a;var d=Math.floor(a%60),e=Math.floor(a/60%60),g=Math.floor(a/3600),h=Math.floor(c/60%60),j=Math.floor(c/3600);if(isNaN(a)||Infinity===a)g=e=d="-";g=0<g||0<j?g+":":"";return g+(((g||10<=h)&&10>e?"0"+e:e)+":")+(10>d?"0"+d:d)};t.ud=function(){document.body.focus();document.onselectstart=r(l)};t.ve=function(){document.onselectstart=r(f)};t.trim=function(a){return(a+"").replace(/^\s+|\s+$/g,"")};t.round=function(a,c){c||(c=0);return Math.round(a*Math.pow(10,c))/Math.pow(10,c)};
t.zb=function(a,c){return{length:1,start:function(){return a},end:function(){return c}}};t.je=function(a){try{var c=window.localStorage||l;c&&(c.volume=a)}catch(d){22==d.code||1014==d.code?t.log("LocalStorage Full (VideoJS)",d):18==d.code?t.log("LocalStorage not allowed (VideoJS)",d):t.log("LocalStorage Error (VideoJS)",d)}};t.Jd=function(a){a.match(/^https?:\/\//)||(a=t.e("div",{innerHTML:'<a href="'+a+'">x</a>'}).firstChild.href);return a};
t.fe=function(a){var c,d,e,g;g="protocol hostname port pathname search hash host".split(" ");d=t.e("a",{href:a});if(e=""===d.host&&"file:"!==d.protocol)c=t.e("div"),c.innerHTML='<a href="'+a+'"></a>',d=c.firstChild,c.setAttribute("style","display:none; position:absolute;"),document.body.appendChild(c);a={};for(var h=0;h<g.length;h++)a[g[h]]=d[g[h]];e&&document.body.removeChild(c);return a};
function D(a,c){var d,e;d=Array.prototype.slice.call(c);e=m();e=window.console||{log:e,warn:e,error:e};a?d.unshift(a.toUpperCase()+":"):a="log";t.log.history.push(d);d.unshift("VIDEOJS:");if(e[a].apply)e[a].apply(e,d);else e[a](d.join(" "))}t.log=function(){D(k,arguments)};t.log.history=[];t.log.error=function(){D("error",arguments)};t.log.warn=function(){D("warn",arguments)};
t.Hd=function(a){var c,d;a.getBoundingClientRect&&a.parentNode&&(c=a.getBoundingClientRect());if(!c)return{left:0,top:0};a=document.documentElement;d=document.body;return{left:t.round(c.left+(window.pageXOffset||d.scrollLeft)-(a.clientLeft||d.clientLeft||0)),top:t.round(c.top+(window.pageYOffset||d.scrollTop)-(a.clientTop||d.clientTop||0))}};t.mc={};t.mc.forEach=function(a,c,d){if(t.h.isArray(a)&&c instanceof Function)for(var e=0,g=a.length;e<g;++e)c.call(d||t,a[e],e,a);return a};
t.ye=function(a,c){var d,e,g,h,j,p,q;"string"===typeof a&&(a={uri:a});videojs.Z.Ea({method:"GET",timeout:45E3},a);c=c||m();p=function(){window.clearTimeout(j);c(k,e,e.response||e.responseText)};q=function(a){window.clearTimeout(j);if(!a||"string"===typeof a)a=Error(a);c(a,e)};d=window.XMLHttpRequest;"undefined"===typeof d&&(d=function(){try{return new window.ActiveXObject("Msxml2.XMLHTTP.6.0")}catch(a){}try{return new window.ActiveXObject("Msxml2.XMLHTTP.3.0")}catch(c){}try{return new window.ActiveXObject("Msxml2.XMLHTTP")}catch(d){}throw Error("This browser does not support XMLHttpRequest.");
});e=new d;e.uri=a.uri;d=t.fe(a.uri);g=window.location;d.protocol+d.host!==g.protocol+g.host&&window.XDomainRequest&&!("withCredentials"in e)?(e=new window.XDomainRequest,e.onload=p,e.onerror=q,e.onprogress=m(),e.ontimeout=m()):(h="file:"==d.protocol||"file:"==g.protocol,e.onreadystatechange=function(){if(4===e.readyState){if(e.te)return q("timeout");200===e.status||h&&0===e.status?p():q()}},a.timeout&&(j=window.setTimeout(function(){4!==e.readyState&&(e.te=f,e.abort())},a.timeout)));try{e.open(a.method||
"GET",a.uri,f)}catch(w){q(w);return}a.withCredentials&&(e.withCredentials=f);a.responseType&&(e.responseType=a.responseType);try{e.send()}catch(ja){q(ja)}};t.Z={};t.Z.Ea=function(a,c){var d,e,g;a=t.h.copy(a);for(d in c)c.hasOwnProperty(d)&&(e=a[d],g=c[d],a[d]=t.h.Ya(e)&&t.h.Ya(g)?t.Z.Ea(e,g):c[d]);return a};
t.a=t.ua.extend({i:function(a,c,d){this.d=a;this.m=t.h.copy(this.m);c=this.options(c);this.K=c.id||c.el&&c.el.id;this.K||(this.K=(a.id&&a.id()||"no_player")+"_component_"+t.p++);this.Vd=c.name||k;this.b=c.el||this.e();this.O=[];this.Ua={};this.Va={};this.Dc();this.H(d);if(c.Qc!==l){var e,g;this.j().reportUserActivity&&(e=t.bind(this.j(),this.j().reportUserActivity),this.c("touchstart",function(){e();this.clearInterval(g);g=this.setInterval(e,250)}),a=function(){e();this.clearInterval(g)},this.c("touchmove",
e),this.c("touchend",a),this.c("touchcancel",a))}}});s=t.a.prototype;s.dispose=function(){this.l({type:"dispose",bubbles:l});if(this.O)for(var a=this.O.length-1;0<=a;a--)this.O[a].dispose&&this.O[a].dispose();this.Va=this.Ua=this.O=k;this.k();this.b.parentNode&&this.b.parentNode.removeChild(this.b);t.Pc(this.b);this.b=k};s.d=f;s.j=n("d");s.options=function(a){return a===b?this.m:this.m=t.Z.Ea(this.m,a)};s.e=function(a,c){return t.e(a,c)};
s.t=function(a){var c=this.d.language(),d=this.d.languages();return d&&d[c]&&d[c][a]?d[c][a]:a};s.w=n("b");s.ma=function(){return this.v||this.b};s.id=n("K");s.name=n("Vd");s.children=n("O");s.Kd=function(a){return this.Ua[a]};s.na=function(a){return this.Va[a]};
s.U=function(a,c){var d,e;"string"===typeof a?(e=a,c=c||{},d=c.componentClass||t.ba(e),c.name=e,d=new window.videojs[d](this.d||this,c)):d=a;this.O.push(d);"function"===typeof d.id&&(this.Ua[d.id()]=d);(e=e||d.name&&d.name())&&(this.Va[e]=d);"function"===typeof d.el&&d.el()&&this.ma().appendChild(d.el());return d};
s.removeChild=function(a){"string"===typeof a&&(a=this.na(a));if(a&&this.O){for(var c=l,d=this.O.length-1;0<=d;d--)if(this.O[d]===a){c=f;this.O.splice(d,1);break}c&&(this.Ua[a.id]=k,this.Va[a.name]=k,(c=a.w())&&c.parentNode===this.ma()&&this.ma().removeChild(a.w()))}};
s.Dc=function(){var a,c,d,e,g,h;a=this;c=a.options();if(d=c.children)if(h=function(d,e){c[d]!==b&&(e=c[d]);e!==l&&(a[d]=a.U(d,e))},t.h.isArray(d))for(var j=0;j<d.length;j++)e=d[j],"string"==typeof e?(g=e,e={}):g=e.name,h(g,e);else t.h.X(d,h)};s.S=r("");
s.c=function(a,c,d){var e,g,h;"string"===typeof a||t.h.isArray(a)?t.c(this.b,a,t.bind(this,c)):(e=t.bind(this,d),h=this,g=function(){h.k(a,c,e)},g.p=e.p,this.c("dispose",g),d=function(){h.k("dispose",g)},d.p=e.p,a.nodeName?(t.c(a,c,e),t.c(a,"dispose",d)):"function"===typeof a.c&&(a.c(c,e),a.c("dispose",d)));return this};
s.k=function(a,c,d){!a||"string"===typeof a||t.h.isArray(a)?t.k(this.b,a,c):(d=t.bind(this,d),this.k("dispose",d),a.nodeName?(t.k(a,c,d),t.k(a,"dispose",d)):(a.k(c,d),a.k("dispose",d)));return this};s.Q=function(a,c,d){var e,g,h;"string"===typeof a||t.h.isArray(a)?t.Q(this.b,a,t.bind(this,c)):(e=t.bind(this,d),g=this,h=function(){g.k(a,c,h);e.apply(this,arguments)},h.p=e.p,this.c(a,c,h));return this};s.l=function(a){t.l(this.b,a);return this};
s.H=function(a){a&&(this.oa?a.call(this):(this.eb===b&&(this.eb=[]),this.eb.push(a)));return this};s.Ka=function(){this.oa=f;var a=this.eb;if(a&&0<a.length){for(var c=0,d=a.length;c<d;c++)a[c].call(this);this.eb=[];this.l("ready")}};s.Xa=function(a){return t.Xa(this.b,a)};s.n=function(a){t.n(this.b,a);return this};s.r=function(a){t.r(this.b,a);return this};s.show=function(){this.b.style.display="block";return this};s.Y=function(){this.b.style.display="none";return this};
function E(a){a.r("vjs-lock-showing")}s.disable=function(){this.Y();this.show=m()};s.width=function(a,c){return F(this,"width",a,c)};s.height=function(a,c){return F(this,"height",a,c)};s.Dd=function(a,c){return this.width(a,f).height(c)};
function F(a,c,d,e){if(d!==b){if(d===k||t.Pd(d))d=0;a.b.style[c]=-1!==(""+d).indexOf("%")||-1!==(""+d).indexOf("px")?d:"auto"===d?"":d+"px";e||a.l("resize");return a}if(!a.b)return 0;d=a.b.style[c];e=d.indexOf("px");return-1!==e?parseInt(d.slice(0,e),10):parseInt(a.b["offset"+t.ba(c)],10)}
function G(a){var c,d,e,g,h,j,p,q;c=0;d=k;a.c("touchstart",function(a){1===a.touches.length&&(d=a.touches[0],c=(new Date).getTime(),g=f)});a.c("touchmove",function(a){1<a.touches.length?g=l:d&&(j=a.touches[0].pageX-d.pageX,p=a.touches[0].pageY-d.pageY,q=Math.sqrt(j*j+p*p),22<q&&(g=l))});h=function(){g=l};a.c("touchleave",h);a.c("touchcancel",h);a.c("touchend",function(a){d=k;g===f&&(e=(new Date).getTime()-c,250>e&&(a.preventDefault(),this.l("tap")))})}
s.setTimeout=function(a,c){function d(){this.clearTimeout(e)}a=t.bind(this,a);var e=setTimeout(a,c);d.p="vjs-timeout-"+e;this.c("dispose",d);return e};s.clearTimeout=function(a){function c(){}clearTimeout(a);c.p="vjs-timeout-"+a;this.k("dispose",c);return a};s.setInterval=function(a,c){function d(){this.clearInterval(e)}a=t.bind(this,a);var e=setInterval(a,c);d.p="vjs-interval-"+e;this.c("dispose",d);return e};
s.clearInterval=function(a){function c(){}clearInterval(a);c.p="vjs-interval-"+a;this.k("dispose",c);return a};t.u=t.a.extend({i:function(a,c){t.a.call(this,a,c);G(this);this.c("tap",this.s);this.c("click",this.s);this.c("focus",this.bb);this.c("blur",this.ab)}});s=t.u.prototype;
s.e=function(a,c){var d;c=t.h.z({className:this.S(),role:"button","aria-live":"polite",tabIndex:0},c);d=t.a.prototype.e.call(this,a,c);c.innerHTML||(this.v=t.e("div",{className:"vjs-control-content"}),this.xb=t.e("span",{className:"vjs-control-text",innerHTML:this.t(this.la)||"Need Text"}),this.v.appendChild(this.xb),d.appendChild(this.v));return d};s.S=function(){return"vjs-control "+t.a.prototype.S.call(this)};s.s=m();s.bb=function(){t.c(document,"keydown",t.bind(this,this.ea))};
s.ea=function(a){if(32==a.which||13==a.which)a.preventDefault(),this.s()};s.ab=function(){t.k(document,"keydown",t.bind(this,this.ea))};t.R=t.a.extend({i:function(a,c){t.a.call(this,a,c);this.td=this.na(this.m.barName);this.handle=this.na(this.m.handleName);this.c("mousedown",this.cb);this.c("touchstart",this.cb);this.c("focus",this.bb);this.c("blur",this.ab);this.c("click",this.s);this.c(a,"controlsvisible",this.update);this.c(a,this.Lc,this.update)}});s=t.R.prototype;
s.e=function(a,c){c=c||{};c.className+=" vjs-slider";c=t.h.z({role:"slider","aria-valuenow":0,"aria-valuemin":0,"aria-valuemax":100,tabIndex:0},c);return t.a.prototype.e.call(this,a,c)};s.cb=function(a){a.preventDefault();t.ud();this.n("vjs-sliding");this.c(document,"mousemove",this.fa);this.c(document,"mouseup",this.qa);this.c(document,"touchmove",this.fa);this.c(document,"touchend",this.qa);this.fa(a)};s.fa=m();
s.qa=function(){t.ve();this.r("vjs-sliding");this.k(document,"mousemove",this.fa);this.k(document,"mouseup",this.qa);this.k(document,"touchmove",this.fa);this.k(document,"touchend",this.qa);this.update()};s.update=function(){if(this.b){var a,c=this.Hb(),d=this.handle,e=this.td;isNaN(c)&&(c=0);a=c;if(d){a=this.b.offsetWidth;var g=d.w().offsetWidth;a=g?g/a:0;c*=1-a;a=c+a/2;d.w().style.left=t.round(100*c,2)+"%"}e&&(e.w().style.width=t.round(100*a,2)+"%")}};
function H(a,c){var d,e,g,h;d=a.b;e=t.Hd(d);h=g=d.offsetWidth;d=a.handle;if(a.options().vertical)return h=e.top,e=c.changedTouches?c.changedTouches[0].pageY:c.pageY,d&&(d=d.w().offsetHeight,h+=d/2,g-=d),Math.max(0,Math.min(1,(h-e+g)/g));g=e.left;e=c.changedTouches?c.changedTouches[0].pageX:c.pageX;d&&(d=d.w().offsetWidth,g+=d/2,h-=d);return Math.max(0,Math.min(1,(e-g)/h))}s.bb=function(){this.c(document,"keydown",this.ea)};
s.ea=function(a){if(37==a.which||40==a.which)a.preventDefault(),this.Xc();else if(38==a.which||39==a.which)a.preventDefault(),this.Yc()};s.ab=function(){this.k(document,"keydown",this.ea)};s.s=function(a){a.stopImmediatePropagation();a.preventDefault()};t.$=t.a.extend();t.$.prototype.defaultValue=0;t.$.prototype.e=function(a,c){c=c||{};c.className+=" vjs-slider-handle";c=t.h.z({innerHTML:'<span class="vjs-control-text">'+this.defaultValue+"</span>"},c);return t.a.prototype.e.call(this,"div",c)};
t.ja=t.a.extend();function ca(a,c){a.U(c);c.c("click",t.bind(a,function(){E(this)}))}t.ja.prototype.e=function(){var a=this.options().rc||"ul";this.v=t.e(a,{className:"vjs-menu-content"});a=t.a.prototype.e.call(this,"div",{append:this.v,className:"vjs-menu"});a.appendChild(this.v);t.c(a,"click",function(a){a.preventDefault();a.stopImmediatePropagation()});return a};t.J=t.u.extend({i:function(a,c){t.u.call(this,a,c);this.selected(c.selected)}});
t.J.prototype.e=function(a,c){return t.u.prototype.e.call(this,"li",t.h.z({className:"vjs-menu-item",innerHTML:this.t(this.m.label)},c))};t.J.prototype.s=function(){this.selected(f)};t.J.prototype.selected=function(a){a?(this.n("vjs-selected"),this.b.setAttribute("aria-selected",f)):(this.r("vjs-selected"),this.b.setAttribute("aria-selected",l))};
t.L=t.u.extend({i:function(a,c){t.u.call(this,a,c);this.Da=this.za();this.U(this.Da);this.P&&0===this.P.length&&this.Y();this.c("keydown",this.ea);this.b.setAttribute("aria-haspopup",f);this.b.setAttribute("role","button")}});s=t.L.prototype;s.wa=l;s.za=function(){var a=new t.ja(this.d);this.options().title&&a.ma().appendChild(t.e("li",{className:"vjs-menu-title",innerHTML:t.ba(this.options().title),re:-1}));if(this.P=this.createItems())for(var c=0;c<this.P.length;c++)ca(a,this.P[c]);return a};
s.ya=m();s.S=function(){return this.className+" vjs-menu-button "+t.u.prototype.S.call(this)};s.bb=m();s.ab=m();s.s=function(){this.Q("mouseout",t.bind(this,function(){E(this.Da);this.b.blur()}));this.wa?I(this):J(this)};s.ea=function(a){a.preventDefault();32==a.which||13==a.which?this.wa?I(this):J(this):27==a.which&&this.wa&&I(this)};function J(a){a.wa=f;a.Da.n("vjs-lock-showing");a.b.setAttribute("aria-pressed",f);a.P&&0<a.P.length&&a.P[0].w().focus()}
function I(a){a.wa=l;E(a.Da);a.b.setAttribute("aria-pressed",l)}t.D=function(a){"number"===typeof a?this.code=a:"string"===typeof a?this.message=a:"object"===typeof a&&t.h.z(this,a);this.message||(this.message=t.D.Bd[this.code]||"")};t.D.prototype.code=0;t.D.prototype.message="";t.D.prototype.status=k;t.D.Wa="MEDIA_ERR_CUSTOM MEDIA_ERR_ABORTED MEDIA_ERR_NETWORK MEDIA_ERR_DECODE MEDIA_ERR_SRC_NOT_SUPPORTED MEDIA_ERR_ENCRYPTED".split(" ");
t.D.Bd={1:"You aborted the video playback",2:"A network error caused the video download to fail part-way.",3:"The video playback was aborted due to a corruption problem or because the video used features your browser did not support.",4:"The video could not be loaded, either because the server or network failed or because the format is not supported.",5:"The video is encrypted and we do not have the keys to decrypt it."};for(var K=0;K<t.D.Wa.length;K++)t.D[t.D.Wa[K]]=K,t.D.prototype[t.D.Wa[K]]=K;
var L,M,N,O;
L=["requestFullscreen exitFullscreen fullscreenElement fullscreenEnabled fullscreenchange fullscreenerror".split(" "),"webkitRequestFullscreen webkitExitFullscreen webkitFullscreenElement webkitFullscreenEnabled webkitfullscreenchange webkitfullscreenerror".split(" "),"webkitRequestFullScreen webkitCancelFullScreen webkitCurrentFullScreenElement webkitCancelFullScreen webkitfullscreenchange webkitfullscreenerror".split(" "),"mozRequestFullScreen mozCancelFullScreen mozFullScreenElement mozFullScreenEnabled mozfullscreenchange mozfullscreenerror".split(" "),"msRequestFullscreen msExitFullscreen msFullscreenElement msFullscreenEnabled MSFullscreenChange MSFullscreenError".split(" ")];
M=L[0];for(O=0;O<L.length;O++)if(L[O][1]in document){N=L[O];break}if(N){t.Sa.Gb={};for(O=0;O<N.length;O++)t.Sa.Gb[M[O]]=N[O]}
t.Player=t.a.extend({i:function(a,c,d){this.I=a;a.id=a.id||"vjs_video_"+t.p++;this.se=a&&t.Ca(a);c=t.h.z(da(a),c);this.Za=c.language||t.options.language;this.Td=c.languages||t.options.languages;this.F={};this.Mc=c.poster||"";this.yb=!!c.controls;a.controls=l;c.Qc=l;P(this,"audio"===this.I.nodeName.toLowerCase());t.a.call(this,this,c,d);this.controls()?this.n("vjs-controls-enabled"):this.n("vjs-controls-disabled");P(this)&&this.n("vjs-audio");t.Fa[this.K]=this;c.plugins&&t.h.X(c.plugins,function(a,
c){this[a](c)},this);var e,g,h,j,p;e=t.bind(this,this.reportUserActivity);this.c("mousedown",function(){e();this.clearInterval(g);g=this.setInterval(e,250)});this.c("mousemove",function(a){if(a.screenX!=j||a.screenY!=p)j=a.screenX,p=a.screenY,e()});this.c("mouseup",function(){e();this.clearInterval(g)});this.c("keydown",e);this.c("keyup",e);this.setInterval(function(){if(this.ta){this.ta=l;this.userActive(f);this.clearTimeout(h);var a=this.options().inactivityTimeout;0<a&&(h=this.setTimeout(function(){this.ta||
this.userActive(l)},a))}},250)}});s=t.Player.prototype;s.language=function(a){if(a===b)return this.Za;this.Za=a;return this};s.languages=n("Td");s.m=t.options;s.dispose=function(){this.l("dispose");this.k("dispose");t.Fa[this.K]=k;this.I&&this.I.player&&(this.I.player=k);this.b&&this.b.player&&(this.b.player=k);this.o&&this.o.dispose();t.a.prototype.dispose.call(this)};
function da(a){var c,d,e={sources:[],tracks:[]};c=t.Ca(a);d=c["data-setup"];d!==k&&t.h.z(c,t.JSON.parse(d||"{}"));t.h.z(e,c);if(a.hasChildNodes()){var g,h;a=a.childNodes;g=0;for(h=a.length;g<h;g++)c=a[g],d=c.nodeName.toLowerCase(),"source"===d?e.sources.push(t.Ca(c)):"track"===d&&e.tracks.push(t.Ca(c))}return e}
s.e=function(){var a=this.b=t.a.prototype.e.call(this,"div"),c=this.I,d;c.removeAttribute("width");c.removeAttribute("height");if(c.hasChildNodes()){var e,g,h,j,p;e=c.childNodes;g=e.length;for(p=[];g--;)h=e[g],j=h.nodeName.toLowerCase(),"track"===j&&p.push(h);for(e=0;e<p.length;e++)c.removeChild(p[e])}d=t.Ca(c);t.h.X(d,function(c){"class"==c?a.className=d[c]:a.setAttribute(c,d[c])});c.id+="_html5_api";c.className="vjs-tech";c.player=a.player=this;this.n("vjs-paused");this.width(this.m.width,f);this.height(this.m.height,
f);c.Md=c.networkState;c.parentNode&&c.parentNode.insertBefore(a,c);t.Jb(c,a);this.b=a;this.c("loadstart",this.Zd);this.c("waiting",this.ee);this.c(["canplay","canplaythrough","playing","ended"],this.de);this.c("seeking",this.be);this.c("seeked",this.ae);this.c("ended",this.Wd);this.c("play",this.Pb);this.c("firstplay",this.Xd);this.c("pause",this.Ob);this.c("progress",this.$d);this.c("durationchange",this.Jc);this.c("fullscreenchange",this.Yd);return a};
function Q(a,c,d){a.o&&(a.oa=l,a.o.dispose(),a.o=l);"Html5"!==c&&a.I&&(t.g.Bb(a.I),a.I=k);a.Ia=c;a.oa=l;var e=t.h.z({source:d,parentEl:a.b},a.m[c.toLowerCase()]);d&&(a.uc=d.type,d.src==a.F.src&&0<a.F.currentTime&&(e.startTime=a.F.currentTime),a.F.src=d.src);a.o=new window.videojs[c](a,e);a.o.H(function(){this.d.Ka()})}s.Zd=function(){this.error(k);this.paused()?(R(this,l),this.Q("play",function(){R(this,f)})):this.l("firstplay")};s.Cc=l;
function R(a,c){c!==b&&a.Cc!==c&&((a.Cc=c)?(a.n("vjs-has-started"),a.l("firstplay")):a.r("vjs-has-started"))}s.Pb=function(){this.r("vjs-paused");this.n("vjs-playing")};s.ee=function(){this.n("vjs-waiting")};s.de=function(){this.r("vjs-waiting")};s.be=function(){this.n("vjs-seeking")};s.ae=function(){this.r("vjs-seeking")};s.Xd=function(){this.m.starttime&&this.currentTime(this.m.starttime);this.n("vjs-has-started")};s.Ob=function(){this.r("vjs-playing");this.n("vjs-paused")};
s.$d=function(){1==this.bufferedPercent()&&this.l("loadedalldata")};s.Wd=function(){this.m.loop?(this.currentTime(0),this.play()):this.paused()||this.pause()};s.Jc=function(){var a=S(this,"duration");a&&(0>a&&(a=Infinity),this.duration(a),Infinity===a?this.n("vjs-live"):this.r("vjs-live"))};s.Yd=function(){this.isFullscreen()?this.n("vjs-fullscreen"):this.r("vjs-fullscreen")};function T(a,c,d){if(a.o&&!a.o.oa)a.o.H(function(){this[c](d)});else try{a.o[c](d)}catch(e){throw t.log(e),e;}}
function S(a,c){if(a.o&&a.o.oa)try{return a.o[c]()}catch(d){throw a.o[c]===b?t.log("Video.js: "+c+" method not defined for "+a.Ia+" playback technology.",d):"TypeError"==d.name?(t.log("Video.js: "+c+" unavailable on "+a.Ia+" playback technology element.",d),a.o.oa=l):t.log(d),d;}}s.play=function(){T(this,"play");return this};s.pause=function(){T(this,"pause");return this};s.paused=function(){return S(this,"paused")===l?l:f};
s.currentTime=function(a){return a!==b?(T(this,"setCurrentTime",a),this):this.F.currentTime=S(this,"currentTime")||0};s.duration=function(a){if(a!==b)return this.F.duration=parseFloat(a),this;this.F.duration===b&&this.Jc();return this.F.duration||0};s.remainingTime=function(){return this.duration()-this.currentTime()};s.buffered=function(){var a=S(this,"buffered");if(!a||!a.length)a=t.zb(0,0);return a};
s.bufferedPercent=function(){var a=this.duration(),c=this.buffered(),d=0,e,g;if(!a)return 0;for(var h=0;h<c.length;h++)e=c.start(h),g=c.end(h),g>a&&(g=a),d+=g-e;return d/a};s.volume=function(a){if(a!==b)return a=Math.max(0,Math.min(1,parseFloat(a))),this.F.volume=a,T(this,"setVolume",a),t.je(a),this;a=parseFloat(S(this,"volume"));return isNaN(a)?1:a};s.muted=function(a){return a!==b?(T(this,"setMuted",a),this):S(this,"muted")||l};s.Ha=function(){return S(this,"supportsFullScreen")||l};s.Fc=l;
s.isFullscreen=function(a){return a!==b?(this.Fc=!!a,this):this.Fc};s.isFullScreen=function(a){t.log.warn('player.isFullScreen() has been deprecated, use player.isFullscreen() with a lowercase "s")');return this.isFullscreen(a)};
s.requestFullscreen=function(){var a=t.Sa.Gb;this.isFullscreen(f);a?(t.c(document,a.fullscreenchange,t.bind(this,function(c){this.isFullscreen(document[a.fullscreenElement]);this.isFullscreen()===l&&t.k(document,a.fullscreenchange,arguments.callee);this.l("fullscreenchange")})),this.b[a.requestFullscreen]()):this.o.Ha()?T(this,"enterFullScreen"):(this.yc(),this.l("fullscreenchange"));return this};
s.requestFullScreen=function(){t.log.warn('player.requestFullScreen() has been deprecated, use player.requestFullscreen() with a lowercase "s")');return this.requestFullscreen()};s.exitFullscreen=function(){var a=t.Sa.Gb;this.isFullscreen(l);if(a)document[a.exitFullscreen]();else this.o.Ha()?T(this,"exitFullScreen"):(this.Db(),this.l("fullscreenchange"));return this};s.cancelFullScreen=function(){t.log.warn("player.cancelFullScreen() has been deprecated, use player.exitFullscreen()");return this.exitFullscreen()};
s.yc=function(){this.Od=f;this.Ed=document.documentElement.style.overflow;t.c(document,"keydown",t.bind(this,this.Ac));document.documentElement.style.overflow="hidden";t.n(document.body,"vjs-full-window");this.l("enterFullWindow")};s.Ac=function(a){27===a.keyCode&&(this.isFullscreen()===f?this.exitFullscreen():this.Db())};s.Db=function(){this.Od=l;t.k(document,"keydown",this.Ac);document.documentElement.style.overflow=this.Ed;t.r(document.body,"vjs-full-window");this.l("exitFullWindow")};
s.selectSource=function(a){for(var c=0,d=this.m.techOrder;c<d.length;c++){var e=t.ba(d[c]),g=window.videojs[e];if(g){if(g.isSupported())for(var h=0,j=a;h<j.length;h++){var p=j[h];if(g.canPlaySource(p))return{source:p,o:e}}}else t.log.error('The "'+e+'" tech is undefined. Skipped browser support check for that tech.')}return l};
s.src=function(a){if(a===b)return S(this,"src");t.h.isArray(a)?U(this,a):"string"===typeof a?this.src({src:a}):a instanceof Object&&(a.type&&!window.videojs[this.Ia].canPlaySource(a)?U(this,[a]):(this.F.src=a.src,this.uc=a.type||"",this.H(function(){window.videojs[this.Ia].prototype.hasOwnProperty("setSource")?T(this,"setSource",a):T(this,"src",a.src);"auto"==this.m.preload&&this.load();this.m.autoplay&&this.play()})));return this};
function U(a,c){var d=a.selectSource(c);d?d.o===a.Ia?a.src(d.source):Q(a,d.o,d.source):(a.setTimeout(function(){this.error({code:4,message:this.t(this.options().notSupportedMessage)})},0),a.Ka())}s.load=function(){T(this,"load");return this};s.currentSrc=function(){return S(this,"currentSrc")||this.F.src||""};s.zd=function(){return this.uc||""};s.Ga=function(a){return a!==b?(T(this,"setPreload",a),this.m.preload=a,this):S(this,"preload")};
s.autoplay=function(a){return a!==b?(T(this,"setAutoplay",a),this.m.autoplay=a,this):S(this,"autoplay")};s.loop=function(a){return a!==b?(T(this,"setLoop",a),this.m.loop=a,this):S(this,"loop")};s.poster=function(a){if(a===b)return this.Mc;a||(a="");this.Mc=a;T(this,"setPoster",a);this.l("posterchange");return this};
s.controls=function(a){return a!==b?(a=!!a,this.yb!==a&&((this.yb=a)?(this.r("vjs-controls-disabled"),this.n("vjs-controls-enabled"),this.l("controlsenabled")):(this.r("vjs-controls-enabled"),this.n("vjs-controls-disabled"),this.l("controlsdisabled"))),this):this.yb};t.Player.prototype.Wb;s=t.Player.prototype;
s.usingNativeControls=function(a){return a!==b?(a=!!a,this.Wb!==a&&((this.Wb=a)?(this.n("vjs-using-native-controls"),this.l("usingnativecontrols")):(this.r("vjs-using-native-controls"),this.l("usingcustomcontrols"))),this):this.Wb};s.da=k;s.error=function(a){if(a===b)return this.da;if(a===k)return this.da=a,this.r("vjs-error"),this;this.da=a instanceof t.D?a:new t.D(a);this.l("error");this.n("vjs-error");t.log.error("(CODE:"+this.da.code+" "+t.D.Wa[this.da.code]+")",this.da.message,this.da);return this};
s.ended=function(){return S(this,"ended")};s.seeking=function(){return S(this,"seeking")};s.ta=f;s.reportUserActivity=function(){this.ta=f};s.Vb=f;s.userActive=function(a){return a!==b?(a=!!a,a!==this.Vb&&((this.Vb=a)?(this.ta=f,this.r("vjs-user-inactive"),this.n("vjs-user-active"),this.l("useractive")):(this.ta=l,this.o&&this.o.Q("mousemove",function(a){a.stopPropagation();a.preventDefault()}),this.r("vjs-user-active"),this.n("vjs-user-inactive"),this.l("userinactive"))),this):this.Vb};
s.playbackRate=function(a){return a!==b?(T(this,"setPlaybackRate",a),this):this.o&&this.o.featuresPlaybackRate?S(this,"playbackRate"):1};s.Ec=l;function P(a,c){return c!==b?(a.Ec=!!c,a):a.Ec}t.Na=t.a.extend();t.Na.prototype.m={Ie:"play",children:{playToggle:{},currentTimeDisplay:{},timeDivider:{},durationDisplay:{},remainingTimeDisplay:{},liveDisplay:{},progressControl:{},fullscreenToggle:{},volumeControl:{},muteToggle:{},playbackRateMenuButton:{}}};t.Na.prototype.e=function(){return t.e("div",{className:"vjs-control-bar"})};
t.ac=t.a.extend({i:function(a,c){t.a.call(this,a,c)}});t.ac.prototype.e=function(){var a=t.a.prototype.e.call(this,"div",{className:"vjs-live-controls vjs-control"});this.v=t.e("div",{className:"vjs-live-display",innerHTML:'<span class="vjs-control-text">'+this.t("Stream Type")+"</span>"+this.t("LIVE"),"aria-live":"off"});a.appendChild(this.v);return a};t.dc=t.u.extend({i:function(a,c){t.u.call(this,a,c);this.c(a,"play",this.Pb);this.c(a,"pause",this.Ob)}});s=t.dc.prototype;s.la="Play";
s.S=function(){return"vjs-play-control "+t.u.prototype.S.call(this)};s.s=function(){this.d.paused()?this.d.play():this.d.pause()};s.Pb=function(){this.r("vjs-paused");this.n("vjs-playing");this.b.children[0].children[0].innerHTML=this.t("Pause")};s.Ob=function(){this.r("vjs-playing");this.n("vjs-paused");this.b.children[0].children[0].innerHTML=this.t("Play")};t.jb=t.a.extend({i:function(a,c){t.a.call(this,a,c);this.c(a,"timeupdate",this.ia)}});
t.jb.prototype.e=function(){var a=t.a.prototype.e.call(this,"div",{className:"vjs-current-time vjs-time-controls vjs-control"});this.v=t.e("div",{className:"vjs-current-time-display",innerHTML:'<span class="vjs-control-text">Current Time </span>0:00',"aria-live":"off"});a.appendChild(this.v);return a};t.jb.prototype.ia=function(){var a=this.d.fb?this.d.F.currentTime:this.d.currentTime();this.v.innerHTML='<span class="vjs-control-text">'+this.t("Current Time")+"</span> "+t.Ba(a,this.d.duration())};
t.kb=t.a.extend({i:function(a,c){t.a.call(this,a,c);this.c(a,"timeupdate",this.ia)}});t.kb.prototype.e=function(){var a=t.a.prototype.e.call(this,"div",{className:"vjs-duration vjs-time-controls vjs-control"});this.v=t.e("div",{className:"vjs-duration-display",innerHTML:'<span class="vjs-control-text">'+this.t("Duration Time")+"</span> 0:00","aria-live":"off"});a.appendChild(this.v);return a};
t.kb.prototype.ia=function(){var a=this.d.duration();a&&(this.v.innerHTML='<span class="vjs-control-text">'+this.t("Duration Time")+"</span> "+t.Ba(a))};t.kc=t.a.extend({i:function(a,c){t.a.call(this,a,c)}});t.kc.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-time-divider",innerHTML:"<div><span>/</span></div>"})};t.rb=t.a.extend({i:function(a,c){t.a.call(this,a,c);this.c(a,"timeupdate",this.ia)}});
t.rb.prototype.e=function(){var a=t.a.prototype.e.call(this,"div",{className:"vjs-remaining-time vjs-time-controls vjs-control"});this.v=t.e("div",{className:"vjs-remaining-time-display",innerHTML:'<span class="vjs-control-text">'+this.t("Remaining Time")+"</span> -0:00","aria-live":"off"});a.appendChild(this.v);return a};t.rb.prototype.ia=function(){this.d.duration()&&(this.v.innerHTML='<span class="vjs-control-text">'+this.t("Remaining Time")+"</span> -"+t.Ba(this.d.remainingTime()))};
t.Oa=t.u.extend({i:function(a,c){t.u.call(this,a,c)}});t.Oa.prototype.la="Fullscreen";t.Oa.prototype.S=function(){return"vjs-fullscreen-control "+t.u.prototype.S.call(this)};t.Oa.prototype.s=function(){this.d.isFullscreen()?(this.d.exitFullscreen(),this.xb.innerHTML=this.t("Fullscreen")):(this.d.requestFullscreen(),this.xb.innerHTML=this.t("Non-Fullscreen"))};t.qb=t.a.extend({i:function(a,c){t.a.call(this,a,c)}});t.qb.prototype.m={children:{seekBar:{}}};
t.qb.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-progress-control vjs-control"})};t.gc=t.R.extend({i:function(a,c){t.R.call(this,a,c);this.c(a,"timeupdate",this.sa);a.H(t.bind(this,this.sa))}});s=t.gc.prototype;s.m={children:{loadProgressBar:{},playProgressBar:{},seekHandle:{}},barName:"playProgressBar",handleName:"seekHandle"};s.Lc="timeupdate";s.e=function(){return t.R.prototype.e.call(this,"div",{className:"vjs-progress-holder","aria-label":"video progress bar"})};
s.sa=function(){var a=this.d.fb?this.d.F.currentTime:this.d.currentTime();this.b.setAttribute("aria-valuenow",t.round(100*this.Hb(),2));this.b.setAttribute("aria-valuetext",t.Ba(a,this.d.duration()))};s.Hb=function(){return this.d.currentTime()/this.d.duration()};s.cb=function(a){t.R.prototype.cb.call(this,a);this.d.fb=f;this.xe=!this.d.paused();this.d.pause()};s.fa=function(a){a=H(this,a)*this.d.duration();a==this.d.duration()&&(a-=0.1);this.d.currentTime(a)};
s.qa=function(a){t.R.prototype.qa.call(this,a);this.d.fb=l;this.xe&&this.d.play()};s.Yc=function(){this.d.currentTime(this.d.currentTime()+5)};s.Xc=function(){this.d.currentTime(this.d.currentTime()-5)};t.nb=t.a.extend({i:function(a,c){t.a.call(this,a,c);this.c(a,"progress",this.update)}});t.nb.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-load-progress",innerHTML:'<span class="vjs-control-text"><span>'+this.t("Loaded")+"</span>: 0%</span>"})};
t.nb.prototype.update=function(){var a,c,d,e,g=this.d.buffered();a=this.d.duration();var h,j=this.d;h=j.buffered();j=j.duration();h=h.end(h.length-1);h>j&&(h=j);j=this.b.children;this.b.style.width=100*(h/a||0)+"%";for(a=0;a<g.length;a++)c=g.start(a),d=g.end(a),(e=j[a])||(e=this.b.appendChild(t.e())),e.style.left=100*(c/h||0)+"%",e.style.width=100*((d-c)/h||0)+"%";for(a=j.length;a>g.length;a--)this.b.removeChild(j[a-1])};t.cc=t.a.extend({i:function(a,c){t.a.call(this,a,c)}});
t.cc.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-play-progress",innerHTML:'<span class="vjs-control-text"><span>'+this.t("Progress")+"</span>: 0%</span>"})};t.Pa=t.$.extend({i:function(a,c){t.$.call(this,a,c);this.c(a,"timeupdate",this.ia)}});t.Pa.prototype.defaultValue="00:00";t.Pa.prototype.e=function(){return t.$.prototype.e.call(this,"div",{className:"vjs-seek-handle","aria-live":"off"})};
t.Pa.prototype.ia=function(){var a=this.d.fb?this.d.F.currentTime:this.d.currentTime();this.b.innerHTML='<span class="vjs-control-text">'+t.Ba(a,this.d.duration())+"</span>"};t.tb=t.a.extend({i:function(a,c){t.a.call(this,a,c);a.o&&a.o.featuresVolumeControl===l&&this.n("vjs-hidden");this.c(a,"loadstart",function(){a.o.featuresVolumeControl===l?this.n("vjs-hidden"):this.r("vjs-hidden")})}});t.tb.prototype.m={children:{volumeBar:{}}};
t.tb.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-volume-control vjs-control"})};t.sb=t.R.extend({i:function(a,c){t.R.call(this,a,c);this.c(a,"volumechange",this.sa);a.H(t.bind(this,this.sa))}});s=t.sb.prototype;s.sa=function(){this.b.setAttribute("aria-valuenow",t.round(100*this.d.volume(),2));this.b.setAttribute("aria-valuetext",t.round(100*this.d.volume(),2)+"%")};s.m={children:{volumeLevel:{},volumeHandle:{}},barName:"volumeLevel",handleName:"volumeHandle"};
s.Lc="volumechange";s.e=function(){return t.R.prototype.e.call(this,"div",{className:"vjs-volume-bar","aria-label":"volume level"})};s.fa=function(a){this.d.muted()&&this.d.muted(l);this.d.volume(H(this,a))};s.Hb=function(){return this.d.muted()?0:this.d.volume()};s.Yc=function(){this.d.volume(this.d.volume()+0.1)};s.Xc=function(){this.d.volume(this.d.volume()-0.1)};t.lc=t.a.extend({i:function(a,c){t.a.call(this,a,c)}});
t.lc.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-volume-level",innerHTML:'<span class="vjs-control-text"></span>'})};t.ub=t.$.extend();t.ub.prototype.defaultValue="00:00";t.ub.prototype.e=function(){return t.$.prototype.e.call(this,"div",{className:"vjs-volume-handle"})};
t.ka=t.u.extend({i:function(a,c){t.u.call(this,a,c);this.c(a,"volumechange",this.update);a.o&&a.o.featuresVolumeControl===l&&this.n("vjs-hidden");this.c(a,"loadstart",function(){a.o.featuresVolumeControl===l?this.n("vjs-hidden"):this.r("vjs-hidden")})}});t.ka.prototype.e=function(){return t.u.prototype.e.call(this,"div",{className:"vjs-mute-control vjs-control",innerHTML:'<div><span class="vjs-control-text">'+this.t("Mute")+"</span></div>"})};
t.ka.prototype.s=function(){this.d.muted(this.d.muted()?l:f)};t.ka.prototype.update=function(){var a=this.d.volume(),c=3;0===a||this.d.muted()?c=0:0.33>a?c=1:0.67>a&&(c=2);this.d.muted()?this.b.children[0].children[0].innerHTML!=this.t("Unmute")&&(this.b.children[0].children[0].innerHTML=this.t("Unmute")):this.b.children[0].children[0].innerHTML!=this.t("Mute")&&(this.b.children[0].children[0].innerHTML=this.t("Mute"));for(a=0;4>a;a++)t.r(this.b,"vjs-vol-"+a);t.n(this.b,"vjs-vol-"+c)};
t.va=t.L.extend({i:function(a,c){t.L.call(this,a,c);this.c(a,"volumechange",this.update);a.o&&a.o.featuresVolumeControl===l&&this.n("vjs-hidden");this.c(a,"loadstart",function(){a.o.featuresVolumeControl===l?this.n("vjs-hidden"):this.r("vjs-hidden")});this.n("vjs-menu-button")}});t.va.prototype.za=function(){var a=new t.ja(this.d,{rc:"div"}),c=new t.sb(this.d,this.m.volumeBar);c.c("focus",function(){a.n("vjs-lock-showing")});c.c("blur",function(){E(a)});a.U(c);return a};
t.va.prototype.s=function(){t.ka.prototype.s.call(this);t.L.prototype.s.call(this)};t.va.prototype.e=function(){return t.u.prototype.e.call(this,"div",{className:"vjs-volume-menu-button vjs-menu-button vjs-control",innerHTML:'<div><span class="vjs-control-text">'+this.t("Mute")+"</span></div>"})};t.va.prototype.update=t.ka.prototype.update;t.ec=t.L.extend({i:function(a,c){t.L.call(this,a,c);this.bd();this.ad();this.c(a,"loadstart",this.bd);this.c(a,"ratechange",this.ad)}});s=t.ec.prototype;s.la="Playback Rate";
s.className="vjs-playback-rate";s.e=function(){var a=t.L.prototype.e.call(this);this.Hc=t.e("div",{className:"vjs-playback-rate-value",innerHTML:1});a.appendChild(this.Hc);return a};s.za=function(){var a=new t.ja(this.j()),c=this.j().options().playbackRates;if(c)for(var d=c.length-1;0<=d;d--)a.U(new t.pb(this.j(),{rate:c[d]+"x"}));return a};s.sa=function(){this.w().setAttribute("aria-valuenow",this.j().playbackRate())};
s.s=function(){for(var a=this.j().playbackRate(),c=this.j().options().playbackRates,d=c[0],e=0;e<c.length;e++)if(c[e]>a){d=c[e];break}this.j().playbackRate(d)};function ea(a){return a.j().o&&a.j().o.featuresPlaybackRate&&a.j().options().playbackRates&&0<a.j().options().playbackRates.length}s.bd=function(){ea(this)?this.r("vjs-hidden"):this.n("vjs-hidden")};s.ad=function(){ea(this)&&(this.Hc.innerHTML=this.j().playbackRate()+"x")};
t.pb=t.J.extend({rc:"button",i:function(a,c){var d=this.label=c.rate,e=this.Oc=parseFloat(d,10);c.label=d;c.selected=1===e;t.J.call(this,a,c);this.c(a,"ratechange",this.update)}});t.pb.prototype.s=function(){t.J.prototype.s.call(this);this.j().playbackRate(this.Oc)};t.pb.prototype.update=function(){this.selected(this.j().playbackRate()==this.Oc)};t.fc=t.u.extend({i:function(a,c){t.u.call(this,a,c);this.update();a.c("posterchange",t.bind(this,this.update))}});s=t.fc.prototype;
s.dispose=function(){this.j().k("posterchange",this.update);t.u.prototype.dispose.call(this)};s.e=function(){var a=t.e("div",{className:"vjs-poster",tabIndex:-1});t.fd||(this.Eb=t.e("img"),a.appendChild(this.Eb));return a};s.update=function(){var a=this.j().poster();this.ga(a);a?this.b.style.display="":this.Y()};s.ga=function(a){var c;this.Eb?this.Eb.src=a:(c="",a&&(c='url("'+a+'")'),this.b.style.backgroundImage=c)};s.s=function(){this.d.play()};t.bc=t.a.extend({i:function(a,c){t.a.call(this,a,c)}});
t.bc.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-loading-spinner"})};t.hb=t.u.extend();t.hb.prototype.e=function(){return t.u.prototype.e.call(this,"div",{className:"vjs-big-play-button",innerHTML:'<span aria-hidden="true"></span>',"aria-label":"play video"})};t.hb.prototype.s=function(){this.d.play()};t.lb=t.a.extend({i:function(a,c){t.a.call(this,a,c);this.update();this.c(a,"error",this.update)}});
t.lb.prototype.e=function(){var a=t.a.prototype.e.call(this,"div",{className:"vjs-error-display"});this.v=t.e("div");a.appendChild(this.v);return a};t.lb.prototype.update=function(){this.j().error()&&(this.v.innerHTML=this.t(this.j().error().message))};
t.q=t.a.extend({i:function(a,c,d){c=c||{};c.Qc=l;t.a.call(this,a,c,d);this.featuresProgressEvents||(this.Ic=f,this.Nc=this.setInterval(function(){var a=this.j().bufferedPercent();this.vd!=a&&this.j().l("progress");this.vd=a;1===a&&this.clearInterval(this.Nc)},500));this.featuresTimeupdateEvents||(a=this.d,this.Nb=f,this.c(a,"play",this.$c),this.c(a,"pause",this.gb),this.Q("timeupdate",function(){this.featuresTimeupdateEvents=f;fa(this)}));var e;e=this.j();a=function(){if(e.controls()&&!e.usingNativeControls()){var a;
this.c("mousedown",this.s);this.c("touchstart",function(){a=this.d.userActive()});this.c("touchmove",function(){a&&this.j().reportUserActivity()});this.c("touchend",function(a){a.preventDefault()});G(this);this.c("tap",this.ce)}};this.H(a);this.c(e,"controlsenabled",a);this.c(e,"controlsdisabled",this.he);this.H(function(){this.networkState&&0<this.networkState()&&this.j().l("loadstart")})}});s=t.q.prototype;
s.he=function(){this.k("tap");this.k("touchstart");this.k("touchmove");this.k("touchleave");this.k("touchcancel");this.k("touchend");this.k("click");this.k("mousedown")};s.s=function(a){0===a.button&&this.j().controls()&&(this.j().paused()?this.j().play():this.j().pause())};s.ce=function(){this.j().userActive(!this.j().userActive())};function fa(a){a.Nb=l;a.gb();a.k("play",a.$c);a.k("pause",a.gb)}s.$c=function(){this.tc&&this.gb();this.tc=this.setInterval(function(){this.j().l("timeupdate")},250)};
s.gb=function(){this.clearInterval(this.tc);this.j().l("timeupdate")};s.dispose=function(){this.Ic&&(this.Ic=l,this.clearInterval(this.Nc));this.Nb&&fa(this);t.a.prototype.dispose.call(this)};s.Tb=function(){this.Nb&&this.j().l("timeupdate")};s.Tc=m();t.q.prototype.featuresVolumeControl=f;t.q.prototype.featuresFullscreenResize=l;t.q.prototype.featuresPlaybackRate=l;t.q.prototype.featuresProgressEvents=l;t.q.prototype.featuresTimeupdateEvents=l;
t.q.dd=function(a){a.Rb=function(c){var d,e=a.Vc;e||(e=a.Vc=[]);d===b&&(d=e.length);e.splice(d,0,c)};a.Rc=function(c){for(var d=a.Vc||[],e,g=0;g<d.length;g++)if(e=d[g].Ta(c))return d[g];return k};a.oc=function(c){var d=a.Rc(c);return d?d.Ta(c):""};a.prototype.Uc=function(c){var d=a.Rc(c);this.Cb();this.k("dispose",this.Cb);this.sc=c;this.Ub=d.Ib(c,this);this.c("dispose",this.Cb)};a.prototype.Cb=function(){this.Ub&&this.Ub.dispose&&this.Ub.dispose()}};
t.g=t.q.extend({i:function(a,c,d){t.q.call(this,a,c,d);for(d=t.g.mb.length-1;0<=d;d--)this.c(t.g.mb[d],this.Fd);(c=c.source)&&(this.b.currentSrc!==c.src||a.I&&3===a.I.Md)&&this.Uc(c);if(t.ic&&a.options().nativeControlsForTouch===f){var e,g,h,j;e=this;g=this.j();c=g.controls();e.b.controls=!!c;h=function(){e.b.controls=f};j=function(){e.b.controls=l};g.c("controlsenabled",h);g.c("controlsdisabled",j);c=function(){g.k("controlsenabled",h);g.k("controlsdisabled",j)};e.c("dispose",c);g.c("usingcustomcontrols",
c);g.usingNativeControls(f)}a.H(function(){this.I&&(this.m.autoplay&&this.paused())&&(delete this.I.poster,this.play())});this.Ka()}});s=t.g.prototype;s.dispose=function(){t.g.Bb(this.b);t.q.prototype.dispose.call(this)};
s.e=function(){var a=this.d,c=a.I,d;if(!c||this.movingMediaElementInDOM===l)c?(d=c.cloneNode(l),t.g.Bb(c),c=d,a.I=k):(c=t.e("video"),t.Sc(c,t.h.z(a.se||{},{id:a.id()+"_html5_api","class":"vjs-tech"}))),c.player=a,t.Jb(c,a.w());d=["autoplay","preload","loop","muted"];for(var e=d.length-1;0<=e;e--){var g=d[e],h={};"undefined"!==typeof a.m[g]&&(h[g]=a.m[g]);t.Sc(c,h)}return c};s.Fd=function(a){"error"==a.type&&this.error()?this.j().error(this.error().code):(a.bubbles=l,this.j().l(a))};s.play=function(){this.b.play()};
s.pause=function(){this.b.pause()};s.paused=function(){return this.b.paused};s.currentTime=function(){return this.b.currentTime};s.Tb=function(a){try{this.b.currentTime=a}catch(c){t.log(c,"Video is not ready. (Video.js)")}};s.duration=function(){return this.b.duration||0};s.buffered=function(){return this.b.buffered};s.volume=function(){return this.b.volume};s.oe=function(a){this.b.volume=a};s.muted=function(){return this.b.muted};s.le=function(a){this.b.muted=a};s.width=function(){return this.b.offsetWidth};
s.height=function(){return this.b.offsetHeight};s.Ha=function(){return"function"==typeof this.b.webkitEnterFullScreen&&(/Android/.test(t.N)||!/Chrome|Mac OS X 10.5/.test(t.N))?f:l};
s.xc=function(){var a=this.b;"webkitDisplayingFullscreen"in a&&this.Q("webkitbeginfullscreen",function(){this.d.isFullscreen(f);this.Q("webkitendfullscreen",function(){this.d.isFullscreen(l);this.d.l("fullscreenchange")});this.d.l("fullscreenchange")});a.paused&&a.networkState<=a.ze?(this.b.play(),this.setTimeout(function(){a.pause();a.webkitEnterFullScreen()},0)):a.webkitEnterFullScreen()};s.Gd=function(){this.b.webkitExitFullScreen()};s.src=function(a){if(a===b)return this.b.src;this.ga(a)};
s.ga=function(a){this.b.src=a};s.load=function(){this.b.load()};s.currentSrc=function(){return this.b.currentSrc};s.poster=function(){return this.b.poster};s.Tc=function(a){this.b.poster=a};s.Ga=function(){return this.b.Ga};s.ne=function(a){this.b.Ga=a};s.autoplay=function(){return this.b.autoplay};s.ie=function(a){this.b.autoplay=a};s.controls=function(){return this.b.controls};s.loop=function(){return this.b.loop};s.ke=function(a){this.b.loop=a};s.error=function(){return this.b.error};
s.seeking=function(){return this.b.seeking};s.ended=function(){return this.b.ended};s.playbackRate=function(){return this.b.playbackRate};s.me=function(a){this.b.playbackRate=a};s.networkState=function(){return this.b.networkState};t.g.isSupported=function(){try{t.A.volume=0.5}catch(a){return l}return!!t.A.canPlayType};t.q.dd(t.g);t.g.V={};
t.g.V.Ta=function(a){function c(a){try{return!!t.A.canPlayType(a)}catch(c){return""}}if(a.type)return c(a.type);a=a.src.match(/\.([^\/\?]+)(\?[^\/]+)?$/i)[1];return c("video/"+a)};t.g.V.Ib=function(a,c){c.ga(a.src)};t.g.V.dispose=m();t.g.Rb(t.g.V);t.g.xd=function(){var a=t.A.volume;t.A.volume=a/2+0.1;return a!==t.A.volume};t.g.wd=function(){var a=t.A.playbackRate;t.A.playbackRate=a/2+0.1;return a!==t.A.playbackRate};t.g.prototype.featuresVolumeControl=t.g.xd();t.g.prototype.featuresPlaybackRate=t.g.wd();
t.g.prototype.movingMediaElementInDOM=!t.kd;t.g.prototype.featuresFullscreenResize=f;t.g.prototype.featuresProgressEvents=f;var V,ga=/^application\/(?:x-|vnd\.apple\.)mpegurl/i,ha=/^video\/mp4/i;
t.g.Kc=function(){4<=t.Xb&&(V||(V=t.A.constructor.prototype.canPlayType),t.A.constructor.prototype.canPlayType=function(a){return a&&ga.test(a)?"maybe":V.call(this,a)});t.od&&(V||(V=t.A.constructor.prototype.canPlayType),t.A.constructor.prototype.canPlayType=function(a){return a&&ha.test(a)?"maybe":V.call(this,a)})};t.g.we=function(){var a=t.A.constructor.prototype.canPlayType;t.A.constructor.prototype.canPlayType=V;V=k;return a};t.g.Kc();t.g.mb="loadstart suspend abort error emptied stalled loadedmetadata loadeddata canplay canplaythrough playing waiting seeking seeked ended durationchange timeupdate progress play pause ratechange volumechange".split(" ");
t.g.Bb=function(a){if(a){a.player=k;for(a.parentNode&&a.parentNode.removeChild(a);a.hasChildNodes();)a.removeChild(a.firstChild);a.removeAttribute("src");if("function"===typeof a.load)try{a.load()}catch(c){}}};
t.f=t.q.extend({i:function(a,c,d){t.q.call(this,a,c,d);var e=c.source;d=c.parentEl;var g=this.b=t.e("div",{id:a.id()+"_temp_flash"}),h=a.id()+"_flash_api",j=a.m,j=t.h.z({readyFunction:"videojs.Flash.onReady",eventProxyFunction:"videojs.Flash.onEvent",errorEventProxyFunction:"videojs.Flash.onError",autoplay:j.autoplay,preload:j.Ga,loop:j.loop,muted:j.muted},c.flashVars),p=t.h.z({wmode:"opaque",bgcolor:"#000000"},c.params),h=t.h.z({id:h,name:h,"class":"vjs-tech"},c.attributes);e&&this.H(function(){this.Uc(e)});
t.Jb(g,d);c.startTime&&this.H(function(){this.load();this.play();this.currentTime(c.startTime)});t.jd&&this.H(function(){this.c("mousemove",function(){this.j().l({type:"mousemove",bubbles:l})})});a.c("stageclick",a.reportUserActivity);this.b=t.f.wc(c.swf,g,j,p,h)}});s=t.f.prototype;s.dispose=function(){t.q.prototype.dispose.call(this)};s.play=function(){this.b.vjs_play()};s.pause=function(){this.b.vjs_pause()};s.src=function(a){return a===b?this.currentSrc():this.ga(a)};
s.ga=function(a){a=t.Jd(a);this.b.vjs_src(a);if(this.d.autoplay()){var c=this;this.setTimeout(function(){c.play()},0)}};t.f.prototype.setCurrentTime=function(a){this.Ud=a;this.b.vjs_setProperty("currentTime",a);t.q.prototype.Tb.call(this)};t.f.prototype.currentTime=function(){return this.seeking()?this.Ud||0:this.b.vjs_getProperty("currentTime")};t.f.prototype.currentSrc=function(){return this.sc?this.sc.src:this.b.vjs_getProperty("currentSrc")};t.f.prototype.load=function(){this.b.vjs_load()};
t.f.prototype.poster=function(){this.b.vjs_getProperty("poster")};t.f.prototype.setPoster=m();t.f.prototype.buffered=function(){return t.zb(0,this.b.vjs_getProperty("buffered"))};t.f.prototype.Ha=r(l);t.f.prototype.xc=r(l);function ia(){var a=W[X],c=a.charAt(0).toUpperCase()+a.slice(1);ka["set"+c]=function(c){return this.b.vjs_setProperty(a,c)}}function la(a){ka[a]=function(){return this.b.vjs_getProperty(a)}}
var ka=t.f.prototype,W="rtmpConnection rtmpStream preload defaultPlaybackRate playbackRate autoplay loop mediaGroup controller controls volume muted defaultMuted".split(" "),ma="error networkState readyState seeking initialTime duration startOffsetTime paused played seekable ended videoTracks audioTracks videoWidth videoHeight textTracks".split(" "),X;for(X=0;X<W.length;X++)la(W[X]),ia();for(X=0;X<ma.length;X++)la(ma[X]);t.f.isSupported=function(){return 10<=t.f.version()[0]};t.q.dd(t.f);t.f.V={};
t.f.V.Ta=function(a){return!a.type?"":a.type.replace(/;.*/,"").toLowerCase()in t.f.Id?"maybe":""};t.f.V.Ib=function(a,c){c.ga(a.src)};t.f.V.dispose=m();t.f.Rb(t.f.V);t.f.Id={"video/flv":"FLV","video/x-flv":"FLV","video/mp4":"MP4","video/m4v":"MP4"};t.f.onReady=function(a){var c;if(c=(a=t.w(a))&&a.parentNode&&a.parentNode.player)a.player=c,t.f.checkReady(c.o)};t.f.checkReady=function(a){a.w()&&(a.w().vjs_getProperty?a.Ka():this.setTimeout(function(){t.f.checkReady(a)},50))};
t.f.onEvent=function(a,c){t.w(a).player.l(c)};t.f.onError=function(a,c){var d=t.w(a).player,e="FLASH: "+c;"srcnotfound"==c?d.error({code:4,message:e}):d.error(e)};
t.f.version=function(){var a="0,0,0";try{a=(new window.ActiveXObject("ShockwaveFlash.ShockwaveFlash")).GetVariable("$version").replace(/\D+/g,",").match(/^,?(.+),?$/)[1]}catch(c){try{navigator.mimeTypes["application/x-shockwave-flash"].enabledPlugin&&(a=(navigator.plugins["Shockwave Flash 2.0"]||navigator.plugins["Shockwave Flash"]).description.replace(/\D+/g,",").match(/^,?(.+),?$/)[1])}catch(d){}}return a.split(",")};
t.f.wc=function(a,c,d,e,g){a=t.f.Ld(a,d,e,g);a=t.e("div",{innerHTML:a}).childNodes[0];d=c.parentNode;c.parentNode.replaceChild(a,c);var h=d.childNodes[0];setTimeout(function(){h.style.display="block"},1E3);return a};
t.f.Ld=function(a,c,d,e){var g="",h="",j="";c&&t.h.X(c,function(a,c){g+=a+"="+c+"&amp;"});d=t.h.z({movie:a,flashvars:g,allowScriptAccess:"always",allowNetworking:"all"},d);t.h.X(d,function(a,c){h+='<param name="'+a+'" value="'+c+'" />'});e=t.h.z({data:a,width:"100%",height:"100%"},e);t.h.X(e,function(a,c){j+=a+'="'+c+'" '});return'<object type="application/x-shockwave-flash" '+j+">"+h+"</object>"};t.f.qe={"rtmp/mp4":"MP4","rtmp/flv":"FLV"};t.f.Le=function(a,c){return a+"&"+c};
t.f.pe=function(a){var c={qc:"",Zc:""};if(!a)return c;var d=a.indexOf("&"),e;-1!==d?e=d+1:(d=e=a.lastIndexOf("/")+1,0===d&&(d=e=a.length));c.qc=a.substring(0,d);c.Zc=a.substring(e,a.length);return c};t.f.Rd=function(a){return a in t.f.qe};t.f.qd=/^rtmp[set]?:\/\//i;t.f.Qd=function(a){return t.f.qd.test(a)};t.f.Sb={};t.f.Sb.Ta=function(a){return t.f.Rd(a.type)||t.f.Qd(a.src)?"maybe":""};t.f.Sb.Ib=function(a,c){var d=t.f.pe(a.src);c.Je(d.qc);c.Ke(d.Zc)};t.f.Rb(t.f.Sb);
t.pd=t.a.extend({i:function(a,c,d){t.a.call(this,a,c,d);if(!a.m.sources||0===a.m.sources.length){c=0;for(d=a.m.techOrder;c<d.length;c++){var e=t.ba(d[c]),g=window.videojs[e];if(g&&g.isSupported()){Q(a,e);break}}}else a.src(a.m.sources)}});t.Player.prototype.textTracks=function(){return this.Ja=this.Ja||[]};
function na(a,c,d,e,g){var h=a.Ja=a.Ja||[];g=g||{};g.kind=c;g.label=d;g.language=e;c=t.ba(c||"subtitles");var j=new window.videojs[c+"Track"](a,g);h.push(j);j.Ab()&&a.H(function(){this.setTimeout(function(){Y(j.j(),j.id())},0)})}function Y(a,c,d){for(var e=a.Ja,g=0,h=e.length,j,p;g<h;g++)j=e[g],j.id()===c?(j.show(),p=j):d&&(j.M()==d&&0<j.mode())&&j.disable();(c=p?p.M():d?d:l)&&a.l(c+"trackchange")}
t.B=t.a.extend({i:function(a,c){t.a.call(this,a,c);this.K=c.id||"vjs_"+c.kind+"_"+c.language+"_"+t.p++;this.Wc=c.src;this.Cd=c["default"]||c.dflt;this.ue=c.title;this.Za=c.srclang;this.Sd=c.label;this.ca=[];this.vb=[];this.pa=this.ra=0;a.c("dispose",t.bind(this,this.vc,this.K))}});s=t.B.prototype;s.M=n("G");s.src=n("Wc");s.Ab=n("Cd");s.title=n("ue");s.language=n("Za");s.label=n("Sd");s.yd=n("ca");s.rd=n("vb");s.readyState=n("ra");s.mode=n("pa");
s.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-"+this.G+" vjs-text-track"})};s.show=function(){oa(this);this.pa=2;t.a.prototype.show.call(this)};s.Y=function(){oa(this);this.pa=1;t.a.prototype.Y.call(this)};s.disable=function(){2==this.pa&&this.Y();this.vc();this.pa=0};function oa(a){0===a.ra&&a.load();0===a.pa&&(a.d.c("timeupdate",t.bind(a,a.update,a.K)),a.d.c("ended",t.bind(a,a.reset,a.K)),("captions"===a.G||"subtitles"===a.G)&&a.d.na("textTrackDisplay").U(a))}
s.vc=function(){this.d.k("timeupdate",t.bind(this,this.update,this.K));this.d.k("ended",t.bind(this,this.reset,this.K));this.reset();this.d.na("textTrackDisplay").removeChild(this)};
s.load=function(){0===this.ra&&(this.ra=1,t.ye(this.Wc,t.bind(this,function(a,c,d){if(a)this.error=a,this.ra=3,this.l("error");else{var e,g;a=d.split("\n");c="";d=1;for(var h=a.length;d<h;d++)if(c=t.trim(a[d])){-1==c.indexOf("--\x3e")?(e=c,c=t.trim(a[++d])):e=this.ca.length;e={id:e,index:this.ca.length};g=c.split(/[\t ]+/);e.startTime=pa(g[0]);e.Aa=pa(g[2]);for(g=[];a[++d]&&(c=t.trim(a[d]));)g.push(c);e.text=g.join("<br/>");this.ca.push(e)}this.ra=2;this.l("loaded")}})))};
function pa(a){var c=a.split(":");a=0;var d,e,g;3==c.length?(d=c[0],e=c[1],c=c[2]):(d=0,e=c[0],c=c[1]);c=c.split(/\s+/);c=c.splice(0,1)[0];c=c.split(/\.|,/);g=parseFloat(c[1]);c=c[0];a+=3600*parseFloat(d);a+=60*parseFloat(e);a+=parseFloat(c);g&&(a+=g/1E3);return a}
s.update=function(){if(0<this.ca.length){var a=this.d.options().trackTimeOffset||0,a=this.d.currentTime()+a;if(this.Qb===b||a<this.Qb||this.$a<=a){var c=this.ca,d=this.d.duration(),e=0,g=l,h=[],j,p,q,w;a>=this.$a||this.$a===b?w=this.Fb!==b?this.Fb:0:(g=f,w=this.Mb!==b?this.Mb:c.length-1);for(;;){q=c[w];if(q.Aa<=a)e=Math.max(e,q.Aa),q.Ra&&(q.Ra=l);else if(a<q.startTime){if(d=Math.min(d,q.startTime),q.Ra&&(q.Ra=l),!g)break}else g?(h.splice(0,0,q),p===b&&(p=w),j=w):(h.push(q),j===b&&(j=w),p=w),d=Math.min(d,
q.Aa),e=Math.max(e,q.startTime),q.Ra=f;if(g)if(0===w)break;else w--;else if(w===c.length-1)break;else w++}this.vb=h;this.$a=d;this.Qb=e;this.Fb=j;this.Mb=p;j=this.vb;p="";a=0;for(c=j.length;a<c;a++)p+='<span class="vjs-tt-cue">'+j[a].text+"</span>";this.b.innerHTML=p;this.l("cuechange")}}};s.reset=function(){this.$a=0;this.Qb=this.d.duration();this.Mb=this.Fb=0};t.Zb=t.B.extend();t.Zb.prototype.G="captions";t.hc=t.B.extend();t.hc.prototype.G="subtitles";t.$b=t.B.extend();t.$b.prototype.G="chapters";
t.jc=t.a.extend({i:function(a,c,d){t.a.call(this,a,c,d);if(a.m.tracks&&0<a.m.tracks.length){c=this.d;a=a.m.tracks;for(var e=0;e<a.length;e++)d=a[e],na(c,d.kind,d.label,d.language,d)}}});t.jc.prototype.e=function(){return t.a.prototype.e.call(this,"div",{className:"vjs-text-track-display"})};t.aa=t.J.extend({i:function(a,c){var d=this.ha=c.track;c.label=d.label();c.selected=d.Ab();t.J.call(this,a,c);this.c(a,d.M()+"trackchange",this.update)}});
t.aa.prototype.s=function(){t.J.prototype.s.call(this);Y(this.d,this.ha.K,this.ha.M())};t.aa.prototype.update=function(){this.selected(2==this.ha.mode())};t.ob=t.aa.extend({i:function(a,c){c.track={M:function(){return c.kind},j:a,label:function(){return c.kind+" off"},Ab:r(l),mode:r(l)};t.aa.call(this,a,c);this.selected(f)}});t.ob.prototype.s=function(){t.aa.prototype.s.call(this);Y(this.d,this.ha.K,this.ha.M())};
t.ob.prototype.update=function(){for(var a=this.d.textTracks(),c=0,d=a.length,e,g=f;c<d;c++)e=a[c],e.M()==this.ha.M()&&2==e.mode()&&(g=l);this.selected(g)};t.T=t.L.extend({i:function(a,c){t.L.call(this,a,c);1>=this.P.length&&this.Y()}});t.T.prototype.ya=function(){var a=[],c;a.push(new t.ob(this.d,{kind:this.G}));for(var d=0;d<this.d.textTracks().length;d++)c=this.d.textTracks()[d],c.M()===this.G&&a.push(new t.aa(this.d,{track:c}));return a};
t.La=t.T.extend({i:function(a,c,d){t.T.call(this,a,c,d);this.b.setAttribute("aria-label","Captions Menu")}});t.La.prototype.G="captions";t.La.prototype.la="Captions";t.La.prototype.className="vjs-captions-button";t.Qa=t.T.extend({i:function(a,c,d){t.T.call(this,a,c,d);this.b.setAttribute("aria-label","Subtitles Menu")}});t.Qa.prototype.G="subtitles";t.Qa.prototype.la="Subtitles";t.Qa.prototype.className="vjs-subtitles-button";
t.Ma=t.T.extend({i:function(a,c,d){t.T.call(this,a,c,d);this.b.setAttribute("aria-label","Chapters Menu")}});s=t.Ma.prototype;s.G="chapters";s.la="Chapters";s.className="vjs-chapters-button";s.ya=function(){for(var a=[],c,d=0;d<this.d.textTracks().length;d++)c=this.d.textTracks()[d],c.M()===this.G&&a.push(new t.aa(this.d,{track:c}));return a};
s.za=function(){for(var a=this.d.textTracks(),c=0,d=a.length,e,g,h=this.P=[];c<d;c++)if(e=a[c],e.M()==this.G)if(0===e.readyState())e.load(),e.c("loaded",t.bind(this,this.za));else{g=e;break}a=this.Da;a===b&&(a=new t.ja(this.d),a.ma().appendChild(t.e("li",{className:"vjs-menu-title",innerHTML:t.ba(this.G),re:-1})));if(g){e=g.ca;for(var j,c=0,d=e.length;c<d;c++)j=e[c],j=new t.ib(this.d,{track:g,cue:j}),h.push(j),a.U(j);this.U(a)}0<this.P.length&&this.show();return a};
t.ib=t.J.extend({i:function(a,c){var d=this.ha=c.track,e=this.cue=c.cue,g=a.currentTime();c.label=e.text;c.selected=e.startTime<=g&&g<e.Aa;t.J.call(this,a,c);d.c("cuechange",t.bind(this,this.update))}});t.ib.prototype.s=function(){t.J.prototype.s.call(this);this.d.currentTime(this.cue.startTime);this.update(this.cue.startTime)};t.ib.prototype.update=function(){var a=this.cue,c=this.d.currentTime();this.selected(a.startTime<=c&&c<a.Aa)};
t.h.z(t.Na.prototype.m.children,{subtitlesButton:{},captionsButton:{},chaptersButton:{}});
if("undefined"!==typeof window.JSON&&"function"===typeof window.JSON.parse)t.JSON=window.JSON;else{t.JSON={};var Z=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;t.JSON.parse=function(a,c){function d(a,e){var j,p,q=a[e];if(q&&"object"===typeof q)for(j in q)Object.prototype.hasOwnProperty.call(q,j)&&(p=d(q,j),p!==b?q[j]=p:delete q[j]);return c.call(a,e,q)}var e;a=String(a);Z.lastIndex=0;Z.test(a)&&(a=a.replace(Z,function(a){return"\\u"+("0000"+
a.charCodeAt(0).toString(16)).slice(-4)}));if(/^[\],:{}\s]*$/.test(a.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:\s*\[)+/g,"")))return e=eval("("+a+")"),"function"===typeof c?d({"":e},""):e;throw new SyntaxError("JSON.parse(): invalid or malformed JSON data");}}
t.nc=function(){var a,c,d,e;a=document.getElementsByTagName("video");c=document.getElementsByTagName("audio");var g=[];if(a&&0<a.length){d=0;for(e=a.length;d<e;d++)g.push(a[d])}if(c&&0<c.length){d=0;for(e=c.length;d<e;d++)g.push(c[d])}if(g&&0<g.length){d=0;for(e=g.length;d<e;d++)if((c=g[d])&&c.getAttribute)c.player===b&&(a=c.getAttribute("data-setup"),a!==k&&videojs(c));else{t.wb();break}}else t.cd||t.wb()};t.wb=function(){setTimeout(t.nc,1)};
"complete"===document.readyState?t.cd=f:t.Q(window,"load",function(){t.cd=f});t.wb();t.ge=function(a,c){t.Player.prototype[a]=c};var qa=this;function $(a,c){var d=a.split("."),e=qa;!(d[0]in e)&&e.execScript&&e.execScript("var "+d[0]);for(var g;d.length&&(g=d.shift());)!d.length&&c!==b?e[g]=c:e=e[g]?e[g]:e[g]={}};$("videojs",t);$("_V_",t);$("videojs.options",t.options);$("videojs.players",t.Fa);$("videojs.TOUCH_ENABLED",t.ic);$("videojs.cache",t.xa);$("videojs.Component",t.a);t.a.prototype.player=t.a.prototype.j;t.a.prototype.options=t.a.prototype.options;t.a.prototype.init=t.a.prototype.i;t.a.prototype.dispose=t.a.prototype.dispose;t.a.prototype.createEl=t.a.prototype.e;t.a.prototype.contentEl=t.a.prototype.ma;t.a.prototype.el=t.a.prototype.w;t.a.prototype.addChild=t.a.prototype.U;
t.a.prototype.getChild=t.a.prototype.na;t.a.prototype.getChildById=t.a.prototype.Kd;t.a.prototype.children=t.a.prototype.children;t.a.prototype.initChildren=t.a.prototype.Dc;t.a.prototype.removeChild=t.a.prototype.removeChild;t.a.prototype.on=t.a.prototype.c;t.a.prototype.off=t.a.prototype.k;t.a.prototype.one=t.a.prototype.Q;t.a.prototype.trigger=t.a.prototype.l;t.a.prototype.triggerReady=t.a.prototype.Ka;t.a.prototype.show=t.a.prototype.show;t.a.prototype.hide=t.a.prototype.Y;
t.a.prototype.width=t.a.prototype.width;t.a.prototype.height=t.a.prototype.height;t.a.prototype.dimensions=t.a.prototype.Dd;t.a.prototype.ready=t.a.prototype.H;t.a.prototype.addClass=t.a.prototype.n;t.a.prototype.removeClass=t.a.prototype.r;t.a.prototype.buildCSSClass=t.a.prototype.S;t.a.prototype.localize=t.a.prototype.t;t.a.prototype.setInterval=t.a.prototype.setInterval;t.a.prototype.setTimeout=t.a.prototype.setTimeout;t.Player.prototype.ended=t.Player.prototype.ended;
t.Player.prototype.enterFullWindow=t.Player.prototype.yc;t.Player.prototype.exitFullWindow=t.Player.prototype.Db;t.Player.prototype.preload=t.Player.prototype.Ga;t.Player.prototype.remainingTime=t.Player.prototype.remainingTime;t.Player.prototype.supportsFullScreen=t.Player.prototype.Ha;t.Player.prototype.currentType=t.Player.prototype.zd;t.Player.prototype.requestFullScreen=t.Player.prototype.requestFullScreen;t.Player.prototype.requestFullscreen=t.Player.prototype.requestFullscreen;
t.Player.prototype.cancelFullScreen=t.Player.prototype.cancelFullScreen;t.Player.prototype.exitFullscreen=t.Player.prototype.exitFullscreen;t.Player.prototype.isFullScreen=t.Player.prototype.isFullScreen;t.Player.prototype.isFullscreen=t.Player.prototype.isFullscreen;$("videojs.MediaLoader",t.pd);$("videojs.TextTrackDisplay",t.jc);$("videojs.ControlBar",t.Na);$("videojs.Button",t.u);$("videojs.PlayToggle",t.dc);$("videojs.FullscreenToggle",t.Oa);$("videojs.BigPlayButton",t.hb);
$("videojs.LoadingSpinner",t.bc);$("videojs.CurrentTimeDisplay",t.jb);$("videojs.DurationDisplay",t.kb);$("videojs.TimeDivider",t.kc);$("videojs.RemainingTimeDisplay",t.rb);$("videojs.LiveDisplay",t.ac);$("videojs.ErrorDisplay",t.lb);$("videojs.Slider",t.R);$("videojs.ProgressControl",t.qb);$("videojs.SeekBar",t.gc);$("videojs.LoadProgressBar",t.nb);$("videojs.PlayProgressBar",t.cc);$("videojs.SeekHandle",t.Pa);$("videojs.VolumeControl",t.tb);$("videojs.VolumeBar",t.sb);$("videojs.VolumeLevel",t.lc);
$("videojs.VolumeMenuButton",t.va);$("videojs.VolumeHandle",t.ub);$("videojs.MuteToggle",t.ka);$("videojs.PosterImage",t.fc);$("videojs.Menu",t.ja);$("videojs.MenuItem",t.J);$("videojs.MenuButton",t.L);$("videojs.PlaybackRateMenuButton",t.ec);t.L.prototype.createItems=t.L.prototype.ya;t.T.prototype.createItems=t.T.prototype.ya;t.Ma.prototype.createItems=t.Ma.prototype.ya;$("videojs.SubtitlesButton",t.Qa);$("videojs.CaptionsButton",t.La);$("videojs.ChaptersButton",t.Ma);
$("videojs.MediaTechController",t.q);t.q.prototype.featuresVolumeControl=t.q.prototype.Ge;t.q.prototype.featuresFullscreenResize=t.q.prototype.Ce;t.q.prototype.featuresPlaybackRate=t.q.prototype.De;t.q.prototype.featuresProgressEvents=t.q.prototype.Ee;t.q.prototype.featuresTimeupdateEvents=t.q.prototype.Fe;t.q.prototype.setPoster=t.q.prototype.Tc;$("videojs.Html5",t.g);t.g.Events=t.g.mb;t.g.isSupported=t.g.isSupported;t.g.canPlaySource=t.g.oc;t.g.patchCanPlayType=t.g.Kc;t.g.unpatchCanPlayType=t.g.we;
t.g.prototype.setCurrentTime=t.g.prototype.Tb;t.g.prototype.setVolume=t.g.prototype.oe;t.g.prototype.setMuted=t.g.prototype.le;t.g.prototype.setPreload=t.g.prototype.ne;t.g.prototype.setAutoplay=t.g.prototype.ie;t.g.prototype.setLoop=t.g.prototype.ke;t.g.prototype.enterFullScreen=t.g.prototype.xc;t.g.prototype.exitFullScreen=t.g.prototype.Gd;t.g.prototype.playbackRate=t.g.prototype.playbackRate;t.g.prototype.setPlaybackRate=t.g.prototype.me;$("videojs.Flash",t.f);t.f.isSupported=t.f.isSupported;
t.f.canPlaySource=t.f.oc;t.f.onReady=t.f.onReady;t.f.embed=t.f.wc;t.f.version=t.f.version;$("videojs.TextTrack",t.B);t.B.prototype.label=t.B.prototype.label;t.B.prototype.kind=t.B.prototype.M;t.B.prototype.mode=t.B.prototype.mode;t.B.prototype.cues=t.B.prototype.yd;t.B.prototype.activeCues=t.B.prototype.rd;$("videojs.CaptionsTrack",t.Zb);$("videojs.SubtitlesTrack",t.hc);$("videojs.ChaptersTrack",t.$b);$("videojs.autoSetup",t.nc);$("videojs.plugin",t.ge);$("videojs.createTimeRange",t.zb);
$("videojs.util",t.Z);t.Z.mergeOptions=t.Z.Ea;t.addLanguage=t.sd;})();
;
videojs.addLanguage("ar",{
 "Play": "تشغيل",
 "Pause": "ايقاف",
 "Current Time": "الوقت الحالي",
 "Duration Time": "Dauer",
 "Remaining Time": "الوقت المتبقي",
 "Stream Type": "نوع التيار",
 "LIVE": "مباشر",
 "Loaded": "تم التحميل",
 "Progress": "التقدم",
 "Fullscreen": "ملء الشاشة",
 "Non-Fullscreen": "غير ملء الشاشة",
 "Mute": "صامت",
 "Unmuted": "غير الصامت",
 "Playback Rate": "معدل التشغيل",
 "Subtitles": "الترجمة",
 "subtitles off": "ايقاف الترجمة",
 "Captions": "التعليقات",
 "captions off": "ايقاف التعليقات",
 "Chapters": "فصول",
 "You aborted the video playback": "لقد ألغيت تشغيل الفيديو",
 "A network error caused the video download to fail part-way.": "تسبب خطأ في الشبكة بفشل تحميل الفيديو بالكامل.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "لا يمكن تحميل الفيديو بسبب فشل في الخادم أو الشبكة ، أو فشل بسبب عدم امكانية قراءة تنسيق الفيديو.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "تم ايقاف تشغيل الفيديو بسبب مشكلة فساد أو لأن الفيديو المستخدم يستخدم ميزات غير مدعومة من متصفحك.",
 "No compatible source was found for this video.": "فشل العثور على أي مصدر متوافق مع هذا الفيديو."
});;
videojs.addLanguage("de",{
 "Play": "Wiedergabe",
 "Pause": "Pause",
 "Current Time": "Aktueller Zeitpunkt",
 "Duration Time": "Dauer",
 "Remaining Time": "Verbleibende Zeit",
 "Stream Type": "Streamtyp",
 "LIVE": "LIVE",
 "Loaded": "Geladen",
 "Progress": "Status",
 "Fullscreen": "Vollbild",
 "Non-Fullscreen": "Kein Vollbild",
 "Mute": "Ton aus",
 "Unmuted": "Ton ein",
 "Playback Rate": "Wiedergabegeschwindigkeit",
 "Subtitles": "Untertitel",
 "subtitles off": "Untertitel aus",
 "Captions": "Untertitel",
 "captions off": "Untertitel aus",
 "Chapters": "Kapitel",
 "You aborted the video playback": "Sie haben die Videowiedergabe abgebrochen.",
 "A network error caused the video download to fail part-way.": "Der Videodownload ist aufgrund eines Netzwerkfehlers fehlgeschlagen.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "Das Video konnte nicht geladen werden, da entweder ein Server- oder Netzwerkfehler auftrat oder das Format nicht unterstützt wird.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "Die Videowiedergabe wurde entweder wegen eines Problems mit einem beschädigten Video oder wegen verwendeten Funktionen, die vom Browser nicht unterstützt werden, abgebrochen.",
 "No compatible source was found for this video.": "Für dieses Video wurde keine kompatible Quelle gefunden."
});;
videojs.addLanguage("es",{
 "Play": "Reproducción",
 "Pause": "Pausa",
 "Current Time": "Tiempo reproducido",
 "Duration Time": "Duración total",
 "Remaining Time": "Tiempo restante",
 "Stream Type": "Tipo de secuencia",
 "LIVE": "DIRECTO",
 "Loaded": "Cargado",
 "Progress": "Progreso",
 "Fullscreen": "Pantalla completa",
 "Non-Fullscreen": "Pantalla no completa",
 "Mute": "Silenciar",
 "Unmuted": "No silenciado",
 "Playback Rate": "Velocidad de reproducción",
 "Subtitles": "Subtítulos",
 "subtitles off": "Subtítulos desactivados",
 "Captions": "Subtítulos especiales",
 "captions off": "Subtítulos especiales desactivados",
 "Chapters": "Capítulos",
 "You aborted the video playback": "Ha interrumpido la reproducción del vídeo.",
 "A network error caused the video download to fail part-way.": "Un error de red ha interrumpido la descarga del vídeo.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "No se ha podido cargar el vídeo debido a un fallo de red o del servidor o porque el formato es incompatible.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "La reproducción de vídeo se ha interrumpido por un problema de corrupción de datos o porque el vídeo precisa funciones que su navegador no ofrece.",
 "No compatible source was found for this video.": "No se ha encontrado ninguna fuente compatible con este vídeo."
});;
videojs.addLanguage("fr",{
 "Play": "Lecture",
 "Pause": "Pause",
 "Current Time": "Temps actuel",
 "Duration Time": "Durée",
 "Remaining Time": "Temps restant",
 "Stream Type": "Type de flux",
 "LIVE": "EN DIRECT",
 "Loaded": "Chargé",
 "Progress": "Progression",
 "Fullscreen": "Plein écran",
 "Non-Fullscreen": "Fenêtré",
 "Mute": "Sourdine",
 "Unmuted": "Son activé",
 "Playback Rate": "Vitesse de lecture",
 "Subtitles": "Sous-titres",
 "subtitles off": "Sous-titres désactivés",
 "Captions": "Sous-titres",
 "captions off": "Sous-titres désactivés",
 "Chapters": "Chapitres",
 "You aborted the video playback": "Vous avez interrompu la lecture de la vidéo.",
 "A network error caused the video download to fail part-way.": "Une erreur de réseau a interrompu le téléchargement de la vidéo.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "Cette vidéo n'a pas pu être chargée, soit parce que le serveur ou le réseau a échoué ou parce que le format n'est pas reconnu.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "La lecture de la vidéo a été interrompue à cause d'un problème de corruption ou parce que la vidéo utilise des fonctionnalités non prises en charge par votre navigateur.",
 "No compatible source was found for this video.": "Aucune source compatible n'a été trouvée pour cette vidéo."
});;
videojs.addLanguage("hu",{
 "Play": "Lejátszás",
 "Pause": "Szünet",
 "Current Time": "Aktuális időpont",
 "Duration Time": "Hossz",
 "Remaining Time": "Hátralévő idő",
 "Stream Type": "Adatfolyam típusa",
 "LIVE": "ÉLŐ",
 "Loaded": "Betöltve",
 "Progress": "Állapot",
 "Fullscreen": "Teljes képernyő",
 "Non-Fullscreen": "Normál méret",
 "Mute": "Némítás",
 "Unmuted": "Némítás kikapcsolva",
 "Playback Rate": "Lejátszási sebesség",
 "Subtitles": "Feliratok",
 "subtitles off": "Feliratok kikapcsolva",
 "Captions": "Magyarázó szöveg",
 "captions off": "Magyarázó szöveg kikapcsolva",
 "Chapters": "Fejezetek",
 "You aborted the video playback": "Leállította a lejátszást",
 "A network error caused the video download to fail part-way.": "Hálózati hiba miatt a videó részlegesen töltődött le.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "A videó nem tölthető be hálózati vagy kiszolgálói hiba miatt, vagy a formátuma nem támogatott.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "A lejátszás adatsérülés miatt leállt, vagy a videó egyes tulajdonságait a böngészője nem támogatja.",
 "No compatible source was found for this video.": "Nincs kompatibilis forrás ehhez a videóhoz."
});;
videojs.addLanguage("it",{
 "Play": "Play",
 "Pause": "Pausa",
 "Current Time": "Orario attuale",
 "Duration Time": "Durata",
 "Remaining Time": "Tempo rimanente",
 "Stream Type": "Tipo del Streaming",
 "LIVE": "LIVE",
 "Loaded": "Caricato",
 "Progress": "Stato",
 "Fullscreen": "Schermo intero",
 "Non-Fullscreen": "Chiudi schermo intero",
 "Mute": "Muto",
 "Unmuted": "Audio",
 "Playback Rate": "Tasso di riproduzione",
 "Subtitles": "Sottotitoli",
 "subtitles off": "Senza sottotitoli",
 "Captions": "Sottotitoli non udenti",
 "captions off": "Senza sottotitoli non udenti",
 "Chapters": "Capitolo",
 "You aborted the video playback": "La riproduzione del filmato è stata interrotta.",
 "A network error caused the video download to fail part-way.": "Il download del filmato è stato interrotto a causa di un problema rete.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "Il filmato non può essere caricato a causa di un errore nel server o nella rete o perché il formato non viene supportato.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "La riproduzione del filmato è stata interrotta a causa di un file danneggiato o per l’utilizzo di impostazioni non supportate dal browser.",
 "No compatible source was found for this video.": "Non ci sono fonti compatibili per questo filmato."
});;
videojs.addLanguage("ja",{
 "Play": "再生",
 "Pause": "一時停止",
 "Current Time": "現在の時間",
 "Duration Time": "長さ",
 "Remaining Time": "残りの時間",
 "Stream Type": "ストリームの種類",
 "LIVE": "ライブ",
 "Loaded": "ロード済み",
 "Progress": "進行状況",
 "Fullscreen": "フルスクリーン",
 "Non-Fullscreen": "フルスクリーン以外",
 "Mute": "ミュート",
 "Unmuted": "ミュート解除",
 "Playback Rate": "再生レート",
 "Subtitles": "サブタイトル",
 "subtitles off": "サブタイトル オフ",
 "Captions": "キャプション",
 "captions off": "キャプション オフ",
 "Chapters": "チャプター",
 "You aborted the video playback": "動画再生を中止しました",
 "A network error caused the video download to fail part-way.": "ネットワーク エラーにより動画のダウンロードが途中で失敗しました",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "サーバーまたはネットワークのエラー、またはフォーマットがサポートされていないため、動画をロードできませんでした",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "破損の問題、またはお使いのブラウザがサポートしていない機能が動画に使用されていたため、動画の再生が中止されました",
 "No compatible source was found for this video.": "この動画に対して互換性のあるソースが見つかりませんでした"
});;
videojs.addLanguage("ko",{
 "Play": "재생",
 "Pause": "일시중지",
 "Current Time": "현재 시간",
 "Duration Time": "지정 기간",
 "Remaining Time": "남은 시간",
 "Stream Type": "스트리밍 유형",
 "LIVE": "라이브",
 "Loaded": "로드됨",
 "Progress": "진행",
 "Fullscreen": "전체 화면",
 "Non-Fullscreen": "전체 화면 해제",
 "Mute": "음소거",
 "Unmuted": "음소거 해제",
 "Playback Rate": "재생 비율",
 "Subtitles": "서브타이틀",
 "subtitles off": "서브타이틀 끄기",
 "Captions": "자막",
 "captions off": "자막 끄기",
 "Chapters": "챕터",
 "You aborted the video playback": "비디오 재생을 취소했습니다.",
 "A network error caused the video download to fail part-way.": "네트워크 오류로 인하여 비디오 일부를 다운로드하지 못 했습니다.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "비디오를 로드할 수 없습니다. 서버 혹은 네트워크 오류 때문이거나 지원되지 않는 형식 때문일 수 있습니다.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "비디오 재생이 취소됐습니다. 비디오가 손상되었거나 비디오가 사용하는 기능을 브라우저에서 지원하지 않는 것 같습니다.",
 "No compatible source was found for this video.": "비디오에 호환되지 않는 소스가 있습니다."
});;
videojs.addLanguage("nl",{
 "Play": "Afspelen",
 "Pause": "Pauze",
 "Current Time": "Huidige Tijd",
 "Duration Time": "Looptijd",
 "Remaining Time": "Resterende Tijd",
 "Stream Type": "Stream Type",
 "LIVE": "LIVE",
 "Loaded": "Geladen",
 "Progress": "Status",
 "Fullscreen": "Volledig scherm",
 "Non-Fullscreen": "Geen volledig scherm",
 "Mute": "Geluid Uit",
 "Unmuted": "Geluid Aan",
 "Playback Rate": "Weergave Rate",
 "Subtitles": "Ondertiteling",
 "subtitles off": "Ondertiteling uit",
 "Captions": "Onderschriften",
 "captions off": "Onderschriften uit",
 "Chapters": "Hoofdstukken",
 "You aborted the video playback": "Je hebt de video weergave afgebroken.",
 "A network error caused the video download to fail part-way.": "De video download is mislukt door een netwerkfout.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "De video kon niet worden geladen, veroorzaakt door een server of netwerkfout of het formaat word niet ondersteund.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "De video weergave is afgebroken omdat deze beschadigd is of de video gebruikt functionaliteit die niet door je browser word ondersteund.",
 "No compatible source was found for this video.": "Voor deze video is geen ondersteunde bron gevonden."
});;
videojs.addLanguage("pt-BR",{
 "Play": "Tocar",
 "Pause": "Pause",
 "Current Time": "Tempo",
 "Duration Time": "Duração",
 "Remaining Time": "Tempo Restante",
 "Stream Type": "Tipo de Stream",
 "LIVE": "AO VIVO",
 "Loaded": "Carregado",
 "Progress": "Progressão",
 "Fullscreen": "Tela Cheia",
 "Non-Fullscreen": "Tela Normal",
 "Mute": "Mudo",
 "Unmuted": "Habilitar Som",
 "Playback Rate": "Velocidade",
 "Subtitles": "Legendas",
 "subtitles off": "Sem Legendas",
 "Captions": "Anotações",
 "captions off": "Sem Anotações",
 "Chapters": "Capítulos",
 "You aborted the video playback": "Você parou a execução de vídeo.",
 "A network error caused the video download to fail part-way.": "Um erro na rede fez o vídeo parar parcialmente.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "O vídeo não pode ser carregado, ou porque houve um problema com sua rede ou pelo formato do vídeo não ser suportado.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "A Execução foi interrompida por um problema com o vídeo ou por seu navegador não dar suporte ao seu formato.",
 "No compatible source was found for this video.": "Não foi encontrada fonte de vídeo compatível."
});;
videojs.addLanguage("ru",{
 "Play": "Воспроизвести",
 "Pause": "Приостановить",
 "Current Time": "Текущее время",
 "Duration Time": "Продолжительность",
 "Remaining Time": "Оставшееся время",
 "Stream Type": "Тип потока",
 "LIVE": "ОНЛАЙН",
 "Loaded": "Загрузка",
 "Progress": "Прогресс",
 "Fullscreen": "Полноэкранный режим",
 "Non-Fullscreen": "Неполноэкранный режим",
 "Mute": "Без звука",
 "Unmuted": "Со звуком",
 "Playback Rate": "Скорость воспроизведения",
 "Subtitles": "Субтитры",
 "subtitles off": "Субтитры выкл.",
 "Captions": "Подписи",
 "captions off": "Подписи выкл.",
 "Chapters": "Главы",
 "You aborted the video playback": "Вы прервали воспроизведение видео",
 "A network error caused the video download to fail part-way.": "Ошибка сети вызвала сбой во время загрузки видео.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "Невозможно загрузить видео из-за сетевого или серверного сбоя либо формат не поддерживается.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "Воспроизведение видео было приостановлено из-за повреждения либо в связи с тем, что видео использует функции, неподдерживаемые вашим браузером.",
 "No compatible source was found for this video.": "Совместимые источники для этого видео отсутствуют."
});;
videojs.addLanguage("uk",{
 "Play": "Відтворити",
 "Pause": "Призупинити",
 "Current Time": "Поточний час",
 "Duration Time": "Тривалість",
 "Remaining Time": "Час, що залишився",
 "Stream Type": "Тип потоку",
 "LIVE": "НАЖИВО",
 "Loaded": "Завантаження",
 "Progress": "Прогрес",
 "Fullscreen": "Повноекранний режим",
 "Non-Fullscreen": "Неповноекранний режим",
 "Mute": "Без звуку",
 "Unmuted": "Зі звуком",
 "Playback Rate": "Швидкість відтворення",
 "Subtitles": "Субтитри",
 "subtitles off": "Без субтитрів",
 "Captions": "Підписи",
 "captions off": "Без підписів",
 "Chapters": "Розділи",
 "You aborted the video playback": "Ви припинили відтворення відео",
 "A network error caused the video download to fail part-way.": "Помилка мережі викликала збій під час завантаження відео.",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "Неможливо завантажити відео через мережевий чи серверний збій або формат не підтримується.",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "Відтворення відео було припинено через пошкодження або у зв'язку з тим, що відео використовує функції, які не підтримуються вашим браузером.",
 "No compatible source was found for this video.": "Сумісні джерела для цього відео відсутні."
});;
videojs.addLanguage("zh",{
 "Play": "播放",
 "Pause": "暂停",
 "Current Time": "当前时间",
 "Duration Time": "时长",
 "Remaining Time": "剩余时间",
 "Stream Type": "媒体流类型",
 "LIVE": "直播",
 "Loaded": "加载完毕",
 "Progress": "进度",
 "Fullscreen": "全屏",
 "Non-Fullscreen": "退出全屏",
 "Mute": "静音",
 "Unmuted": "取消静音",
 "Playback Rate": "播放码率",
 "Subtitles": "字幕",
 "subtitles off": "字幕关闭",
 "Captions": "内嵌字幕",
 "captions off": "内嵌字幕关闭",
 "Chapters": "节目段落",
 "You aborted the video playback": "视频播放被终止",
 "A network error caused the video download to fail part-way.": "网络错误导致视频下载中途失败。",
 "The video could not be loaded, either because the server or network failed or because the format is not supported.": "视频因格式不支持或者服务器或网络的问题无法加载。",
 "The video playback was aborted due to a corruption problem or because the video used features your browser did not support.": "由于视频文件损坏或是该视频使用了你的浏览器不支持的功能，播放终止。",
 "No compatible source was found for this video.": "无法找到此视频兼容的源。",
 "The video is encrypted and we do not have the keys to decrypt it.": "视频已加密，无法解密。"
});;
$(function () {
    /* Vars */
    var bodMobileContainer = '.bod-mobile-bio',
        mobileLinkWrapper = '.bod-wrapper .mobile-link',
        mobileLink = mobileLinkWrapper + ' span',
        breadcrumbsWrapper = '.breadcrumbs-wrapper';
    
    /* Helper Functions */
    function isMobile() {
        return $(mobileLink).length && $($(mobileLink)[0]).is(':visible');
    }

    // sets the mobile bio page by removing other page elements and only showing the overlay content
    function setMobileBioPage($overlay) {

        // remove close-on-doc-click class, as it's not an overlay
        $overlay.removeClass('close-on-doc-click');

        // store overlay html
        var overlayHTML = $overlay.clone().wrap('<p>').parent().html(); // gets overaly html, including parent overlay div
        var backHTML = '<a href="" class="back"><span class="icon-angle-left"></span><span>BACK</span></a>';

        // hide every inner content component
        $('.tertiary-container .container-fluid').children().hide();

        // insert overlay to bod-mobile-bio container and show
        $(bodMobileContainer).prepend(overlayHTML).fadeIn();

        // set the breadcrumb to '< BACK' and add event click that redirects to same page to get back to all bod content + add this page to history so that native back button goes to correct url?
        $(breadcrumbsWrapper).html(backHTML);
    }

    // sets the overlay popup for tablet/desktop
    function setOverlayBio($overlay) {

        // first fade out all overlays if one is open
        $('.member-overlay').fadeOut();

        $overlay.addClass('active').addClass('close-on-doc-click');
        $overlay.show();

        // TODO: check page scroll to see if the popup should go down instead of up
    }

    /* Functions */
    function init() {

        // opening overlay
        $('.bod-wrapper .mobile-link span, .bod-wrapper .short-name a').on('click', function (e) {
            e.preventDefault();

            var $overlay = $(this).closest('.member-block').find('.member-overlay');

            if ($overlay.length) {

                if (isMobile()) {
                    setMobileBioPage($overlay);
                } else {
                    setOverlayBio($overlay);
                }
            }

            e.stopPropagation();
            //return false;
        });

        // overlay close
        $('.overlay-close span').on('click', function (e) {
            $(this).parent().parent().fadeOut();
        });

        // preventing clicks from bubbling up DOM so that a click outside the overlay will close it
        $('.member-overlay').on('click', function (e) {
            e.stopPropagation();
        });
    }

    init();
});;
$(function () {
    var subNav = '.sub-nav-container > ul',
        sitemapBlock = '.sitemap .toggle-wrapper',
        contentBlockTwoCol = '.content-block.two-column',
        linksBoxPageLinks = '.links-box .page-links .page-links-wrapper';
    
    $(subNav).columnize({
        columns: 2,
        buildOnce: true         // don't run on re-size
    }).find('li').css('padding-top', '10px');

    $(sitemapBlock).columnize({columns: 2, lastNeverTallest: true});
    $(contentBlockTwoCol).columnize({columns: 2});
    $(linksBoxPageLinks).columnize({columns: 2});
});;
$(function () {
    var featuredHighlightWrapper = '.featured-highlight',
        highlight = featuredHighlightWrapper + " .toggle-wrapper > ul > li";

    // sets the width of each highlight overlay based on the current image
    function setOverlayWidths() {
        if (helperFunctions.exists($(featuredHighlightWrapper))) {

            var $highlights = $(highlight);
            $highlights.each(function () {

                // check if even has overlay first
                var $this = $(this);
                var $overlay = $this.find('.overlay-content');
                if (helperFunctions.exists($overlay)) {

                    // if icon exists, override date title styling
                    var $image = $($this.find('img.img-responsive')[0]);
                    if (helperFunctions.exists($image)) {
                        var $dateTitle = $this.find('.date-title');
                        $dateTitle.css('width', '80%');
                        $dateTitle.css('float', 'left');

                        // now set overlay width only if the image doesn't fill the list item container
                        if ($this.outerWidth() > $image.width()) {

                            var imgWidth = $image.width();

                            // set overlay width - overlay padding sides
                            var paddingLeft = $overlay.css('padding-left').replace("px", "");
                            var paddingRight = $overlay.css('padding-right').replace("px", "");
                            $overlay.width(imgWidth - paddingLeft - paddingRight);

                            // set overlay offset to match image inside highlight
                            var offset = ($this.width() - imgWidth) / 2;
                            $overlay.css('margin-left', offset);   // overlay is absolute
                        }
                    }
                }
            });
        }
    }

    // if ie8, set overlay widths on doc ready and on window resize
    setOverlayWidths();
    $(window).resize(function () {
        setOverlayWidths();
    });
});
;
$(function () {
    /* Functions */

    // document click event for if an event bubbles to the body, in which case any element with that class will fade out
    $('body').click(function (e) {
        $('.close-on-doc-click').fadeOut();

        if (helperFunctions.exists($('#ui-datepicker-div'))) {
            $('#ui-datepicker-div').css('visibility', 'hidden');
        }
    });

    // language links
    function setLanguagePicker() {
        $('.language-picker a.selected-language').click(function (e) {
            var $this = $(this);
            $this.next().toggle();
            e.stopPropagation();
            e.preventDefault();
        });

        $('.language-picker .picker ul li a').click(function (e) {
            var $this = $(this);
            if ($this.hasClass('active')) {
                $('.language-picker .picker').toggle();
            }
        });

        $('.open-language-picker').on('click', function (e) {
            $(this).parent().find('.close-on-doc-click').toggle();

            if (e.target.nodeName == "a" || e.target.nodeName == "A") {
                if ($(e.target).hasClass('active')) {
                    e.stopPropagation();
                    e.preventDefault();
                } else {
                    return;
                }
            } else {
                e.stopPropagation();
                e.preventDefault();
            }
        });
    }

    // Remove Logo box if empty
    $(document).ready(function () {
        if ($.trim($(".logo-two").html()).length == 0)
            $(".logo-two").hide();
    });

    //Kaltura video player resize functinality
    function initializeVideoPlayer() {
        $('ul.video-size li > a').click(function (e) {
            $(this).closest(".video-options-block").find("select.video-size-group option:first").text(this.innerText);
            var $videoJs = $('.video-js');
            e.preventDefault();
            var newSize = $(this).attr('data-size');
            $videoJs.attr('style', 'width: ' + newSize + '%');
        });
        $('.video-options-block select').on('mousedown', function (e) {
            e.preventDefault();
            this.blur();
            window.focus();
        });
    }

    // sets all overlay postions (vertical only for now) that use the click and hover classes (define overlay styling per component)
    var DynamicOverlay = {
        clickClass: ".overlay-click",
        hoverClass: ".overlay-hover",
        overlayClass: ".dynamic-overlay",

        setClickAction: function () {
            $(this.clickClass).click(function (e) {
                DynamicOverlay.handleOverlayPosition($(this));
            });
        },
        setHoverAction: function () {
            var obj = this;

            $(this.hoverClass)
                .mouseenter(function () {
                    clearTimeout($(this).data("hover-timer"));
                    DynamicOverlay.handleOverlayPosition($(this));
                })
                .mouseleave(function () {
                    var $parent = $(this).parent();
                    $(this).data("hover-timer", setTimeout(function () {
                        var $overlay = $parent.find(obj.overlayClass);
                        if ($parent.find(obj.overlayClass + ":hover").length === 0) {
                            if (helperFunctions.exists($overlay)) {
                                $overlay.hide();
                            }
                        }
                    }, 500));
                });

            $(this.overlayClass)
                .mouseleave(function () {
                    $(this).hide();
                })
                .click(function (e) {
                    if (!$(e.target).is("a"))
                        $(this).hide();
                });
        },
        handleOverlayPosition: function ($el) {

            var $overlay = $el.parent().find(this.overlayClass);           // overlay must have this class to be found
            var $elContainer = $el.closest(".dynamic-overlay-container");   // container must have this class to be found

            if ($overlay && $elContainer) {
                $elContainer.closest("ul").find(this.overlayClass).hide();
                var bottomOffset = $elContainer.outerHeight();  // all overlays with an :after element will have margin-bottom to fill missing space from the quote-icon

                $overlay.css("bottom", bottomOffset + "px");
                $overlay.show();
            }
        },

        init: function () {
            this.setClickAction();
            this.setHoverAction();
        }
    }

    // binding key events for WCAG compliance (section 1.3.1)
    function bindKeyEvents() {
        $(document).keydown(function (e) {

            // spare the air docked alert
            if ($('.spare-the-air-docked-alert') != undefined && $('.spare-the-air-docked-alert').is(':focus') && e.keyCode === 68) // d key 
            {
                $('.spare-the-air-docked-alert .docked-bar span').trigger('tap');       // toggle docked alert
                return false;
            }
        });
    }

    // event handlers last
    setLanguagePicker();
    initializeVideoPlayer();
    bindKeyEvents();

    DynamicOverlay.init();
});;
$(function () {
    var carouselId = '#carousel-example';
    $(carouselId).on('slide.bs.carousel', function (e) {
        var $e = $(e.relatedTarget);
        var idx = $e.index();
        var itemsPerSlide = 4;
        var totalItems = $(carouselId + ' .item').length;
        if (idx >= totalItems - (itemsPerSlide - 1)) {
            var it = itemsPerSlide - (totalItems - idx);
            for (var i = 0; i < it; i++) {
                // append slides to end
                if (e.direction == "left") {
                    $(carouselId + ' .item').eq(i).appendTo('.carousel-inner');
                } else {
                    $(carouselId + ' .item').eq(0).appendTo('.carousel-inner');
                }
            }
        }
    });
});;
$(function () {
    if (window._modalPages?.length) {
        const tempArr = [];
        for (const mp of window._modalPages) {
            tempArr.push(new ModalPage(mp.modalId, mp.contextItem, mp.closeConfirm, mp.formId));
        }
        window._modalPages = tempArr;

    }
});

class ModalPage {
    
    urlParam = "modal";
    modal;
    $modal;
    hasForm;
    $loading;
    itemId;
    contextItem;

    constructor(modalId, contextItem, closeConfirmText, formId) {
        this.closeConfirmText = closeConfirmText;
        this.modal = document.getElementById(modalId);
        this.$modal = $(this.modal);
        this.contextItem = contextItem;
        this.hasForm = !!this.$modal.find("form").length;
        this.$loading = this.$modal.find(".form-loading");

        const $formContainer = this.$modal.find("div.form-placeholder");
        let renderFormAsync = !!$formContainer.length && !!formId.length;
        this.$modal.on('show.bs.modal', evt => {
            if (renderFormAsync) {
                this.hasForm = true;
                this.$loading.show();
                const $this = this;
                BaaqmdSessionManager.sessionPopulate(function (formRenderUrl) {
                    $formContainer.empty().load(formRenderUrl + formId, function () {
                        renderFormAsync = false;
                        eval($formContainer.find("form").data("ajax-success"));
                        $this.onModalShow(evt);
                        $this.$loading.hide();
                    });
                });
            } else {
                this.onModalShow(evt);
            }
        });
        this.$modal.find(".close-button").click((evt) => this.onModalClose(evt));

        const urlParams = new URLSearchParams(window.location.search);
        const targetModalToPopup = urlParams.get(this.urlParam);
        if (targetModalToPopup && targetModalToPopup === modalId) {
            this.$modal.modal("show");
        }
    }

    onModalShow(event) {
        this.itemId = $(event.relatedTarget).data("item");
        this.populateDataboundFields();
        const $this = this;
        if (this.hasForm) {
            document.addEventListener('submit', function (evt) {
                evt.preventDefault();
                $this.$loading.show();

                $(document).ajaxStop(function () {
                    $this.$loading.hide();
                    $this.$modal[0].scrollTop = 0;
                    $(document).unbind("ajaxStop");
                    $this.hasForm = !!$this.getVisibleInputs().length;
                    $this.populateDataboundFields();
                });
            });
        }
    }

    onModalClose(evt) {
        if (this.hasForm) {
            const confirmAlert = confirm("\n" + this.closeConfirmText);
            if (confirmAlert === true) {
                this.hideModal();
            }
        } else {
            this.hideModal();
        }
    }

    hideModal() {
        try {
            this.$modal.modal("hide");
        } catch (e) {
            try {
                bootstrap.Modal.getInstance(this.modal).hide();
            } catch {
                this.$modal.hide();
                $('.modal-backdrop').hide();
            }
            console.log(e);
        }
        if (this.hasForm) {
            this.getVisibleInputs().each((i, el) => {
                $(el).val("");
            });
        }
    }

    getVisibleInputs() {
        return this.$modal.find("form :input:not(:button, :submit):visible");
    }

    populateDataboundFields() {
        if (this.hasForm && this.itemId?.length) {
            const handlers = this.$modal.find("form").data("databoundTextHandlers");
            if (handlers) {
                for (const handler of handlers) {
                    handler(this.itemId, this.contextItem);
                }
            }
        }
    }
};
$(function() {
    var desktopSideNavToggler = '.side-nav-sections span.toggle-icon',
        deviceSectionMenuLink = '.tablet-section-menu .device-section-menu-link',
        deviceSectionMenuToggler = '.tablet-section-menu .section-dropdown span.toggle-icon',
        currentPageLink = '.side-nav-menu li.current > p a, .tablet-section-menu li.current > p a';

    // desktop side nav menu toggle
    function setSideNavigationMenuToggle() {
        $(desktopSideNavToggler).click(function (e) {

            var $this = $(this);

            $this.toggleClass('icon-angle-up');
            $this.toggleClass('icon-angle-down');

            var $hiddenContent = $this.parent().next();
            var $menuItem = $hiddenContent.parent();

            if ($hiddenContent.length > 0) {
                $hiddenContent.toggle();

                $menuItem.toggleClass('active');
            }

            e.stopPropagation();
        });
    }

    // device section dropdown and sub-page dropdown toggles
    function setDeviceSectionMenuToggle() {
        // device section dropdown toggle
        $(deviceSectionMenuLink).click(function (e) {

            var tabletSectionMenu = $(this).parent();
            tabletSectionMenu.toggleClass('active');

            e.stopPropagation();
            return false;
        });
        // sub-page dropdown toggle
        $(deviceSectionMenuToggler).click(function (e) {

            var $this = $(this);
            $this.toggleClass('icon-angle-down');
            $this.toggleClass('icon-angle-up');

            $this.parent().next().toggle();
        });
    }

    function disableCurrentPageClick() {
        $(currentPageLink).click(function (e) {
            e.stopPropagation();
            return false;
        });
    }

    function setDeviceFlyoutNavigation() {

        var $menulink = $('.device-menu-link'),
            $wrap = $('.wrap'),
            $navFlyout = $('#device-navigation-flyout'),
            $navClose = $('.nav-device-back');

        $menulink.add($navClose).click(function (e) {
            $menulink.toggleClass('device-nav-active');
            $wrap.toggleClass('device-nav-active');
            $navFlyout.toggleClass('device-nav-active');

            e.stopPropagation();
            return false;
        });
    }


    // mobile blocks toggle
    function setMobileToggleBlocks() {

        var $toggler = $('.mobile-block span.toggle-icon, .webcasts-module span.toggle-icon');

        // on load, set toggle state
        $toggler.each(function () {

            var $this = $(this);
            if ($this.hasClass('icon-plus')) {
                $this.parent().next().addClass('hide');
            }

        });

        // on tap
        $toggler.click(function (e) {

            var $this = $(this);
            var toggleWrapper = $this.parent().parent().find('.toggle-wrapper');

            if (toggleWrapper.length > 0 && toggleWrapper.hasClass('toggle-wrapper')) {
                if ($this.hasClass('icon-minus')) {

                    toggleWrapper.addClass('hide');
                    $this.removeClass('icon-minus');
                    $this.addClass('icon-plus');

                } else { // display content
                    toggleWrapper.removeClass('hide');
                    $this.addClass('icon-minus');
                    $this.removeClass('icon-plus');
                }
            }
            e.stopPropagation();
            return false;
        });
    }

    function setDesktopMainNavigation() {

        // set aria-hidden
        $('.main-navigation .menu-item').hover(
            function () {
                $(this).find('.sub-nav-wrapper').attr('aria-hidden', 'false');
            }, function () {
                $(this).find('.sub-nav-wrapper').attr('aria-hidden', 'true');
            });

        // prevent click up
        $('.main-navigation .menu-item > a').click(function (e) {
            var url = $(this).attr('href');
            if (url === "#") {
                e.stopPropagation();
                return false;
            }
        });
    }

    function setDeviceMainNavigationToggle() {
        $('.device-main-navigation > ul > li > a').click(function (e) {
            var $this = $(this);

            // if empty, return true to redirect
            if ($this.hasClass('empty')) {
                return true;
            } else {
                if ($this.hasClass('active')) {

                    $this.removeClass('active');
                    $this.find('span').removeClass('icon-chevron-up');
                    $this.find('span').addClass('icon-chevron-down');

                    $this.next().slideUp();
                } else {

                    $this.addClass('active');
                    $this.find('span').removeClass('icon-chevron-down');
                    $this.find('span').addClass('icon-chevron-up');

                    $this.next().slideDown();
                }
                e.stopPropagation();
                return false;
            }
        });
    }

    function setDesktopTopNavigation() {

        // set aria-hidden
        $('.top-nav-links .menu-item').hover(
            function () {
                $(this).find('.sub-nav-wrapper').attr('aria-hidden', 'false');
            }, function () {
                $(this).find('.sub-nav-wrapper').attr('aria-hidden', 'true');
            });

        // prevent click up
        $('.top-nav-links .menu-item > a').click(function (e) {
            var url = $(this).attr('href');
            if (url === "#") {
                e.stopPropagation();
                return false;
            }
        });
    }

    setSideNavigationMenuToggle();
    setDeviceSectionMenuToggle();
    disableCurrentPageClick();

    setDesktopMainNavigation();
    setDeviceFlyoutNavigation();
    setDesktopTopNavigation();
    setMobileToggleBlocks();
    setDeviceMainNavigationToggle();
});;
$(function () {

    var searchFilters = '.search-result-filters',
        searchFiltersModalBackground = '.search-result-filters-background',
        deviceSearchFiltersLink = '.filter-action-wrapper > a',
        clearFilters = 'a.clear-filters',
        filterCheckboxes = searchFilters + ' input[type="checkbox"]',
        modalDone = 'a.done';

    // sets device filter action to open filters as a modal and close when done
    function setDeviceSearchFiltersModalActions() {

        $(deviceSearchFiltersLink + ", " + modalDone).click(function (e) {
            var $modal = $(searchFilters);
            var $modalBackground = $(searchFiltersModalBackground);

            $modal.parent().toggle();
            $($modal.parent().find(".side-nav-menu[data-nav='sideNavigationMenu']")).toggle();
            $modal.toggleClass("active");
            $modalBackground.toggleClass("active");

            e.stopPropagation();    // stop bubbling so that user can only close modal on 'done' button
            return false;
        });
    }

    // sets tap listener for clearing all filters (works for all breakpoints)
    function setClearFilters() {

        $(clearFilters).click(function (e) {

            $this = $(this);

            $(filterCheckboxes).each(function (index) {

                $(this).prop('checked', false);
                //$(this).attr("disabled", "disabled");
                $(this).next().removeClass('active');
            });

            e.stopPropagation();
            return false;
        });
    }

    function supportIE8Checkboxes() {
        if ($('.ie8').length > 0) {
            $('.search-result-filters input + label').click(function (e) {

                $this = $(this);
                $this.toggleClass('active');

                if ($this.prev().is(':checked')) {
                    $this.find('span').css('background-position-y', '0')
                } else {
                    $this.find('span').css('background-position-y', '-17px')
                }

                e.stopPropagation();
            });
        }
    }

    setDeviceSearchFiltersModalActions();
    setClearFilters();
    supportIE8Checkboxes();
});;
$(function () {

    var $dockedAlert = $(".spare-the-air-docked-alert"),
        $dockedAlertToggler = $dockedAlert.find(".dockbar-td"),
        newVisitorDelay = 5000;

    /* functions */
    function setDockToggle() {
        var compToggleWidth = (($dockedAlert.find(".toggle-wrapper").outerWidth()) * -1) + "px";

        $dockedAlert.click(function (e) {
            if (!$(e.target).is("a"))
                $dockedAlertToggler.click();
        });

        $dockedAlertToggler.click(function (e) {
            var $this = $(this);
            if (!$this.is(":animated")) {   // prevent double click while animating
                $this.find("span").toggleClass("icon-ArrowRight");
                $this.find("span").toggleClass("icon-ArrowLeft");

                var compRightPos = $dockedAlert.css("right");
                if (compRightPos === compToggleWidth) {     // closed state
                    $dockedAlert.animate({"right": 0});
                } else {
                    $dockedAlert.animate({"right": compToggleWidth});
                }
            }

            e.stopPropagation();
        });
    }

    function handleIsNewVisitor() {

        if (localStorage.getItem("old_visitor")) {
            return true;
        } else {
            // new visitor, show docked alert expanded for X seconds
            $dockedAlertToggler.click();
            setTimeout(function () {
                $dockedAlertToggler.click();
            }, newVisitorDelay);

            localStorage.setItem("old_visitor", 1);
        }
    }

    setDockToggle();
    handleIsNewVisitor();
});;
$(function () {
    var PlayerWidget = {

        playerClass: '.video-player .video-js',
        videoSizeBtnClass: '.video-size a',
        swfPath: '/Presentation/DotGov/includes/_js/libs/video/support/video-js.swf',
        aspectRatio: 9 / 16,
        players: [],

        // sets global player settings such as default flash fallback path
        setGlobalPlayerSettings: function () {
            videojs.options.flash.swf = PlayerWidget.swfPath;
        },

        // initialize all players and hide certain components
        bindPlayers: function () {

            $(PlayerWidget.playerClass).each(function () {

                videojs(this.id).ready(function () {

                    PlayerWidget.players.push(this);    // add player to array for window resize accessibility
                    PlayerWidget.createPlayIcon(this);

                    // if IE8, use JS to resize based on aspect ratio
                    if (helperFunctions.isIE8()) {
                        PlayerWidget.resizeVideoJS(this);

                        // set window resize for responsive
                        $(window).resize(function () {
                            $(PlayerWidget.players).each(function () {
                                PlayerWidget.resizeVideoJS(this);
                            });
                        });
                    } else {
                        // remove width attribute from video for resize button changes
                        this.I.parentElement.style.width = "";
                    }
                });
            });

            PlayerWidget.handleOnSizeChange();
        },

        // handles the call to change the player size
        handleOnSizeChange: function () {
            $(PlayerWidget.videoSizeBtnClass).click(function (e) {

                var $this = $(this);
                var size = $this.attr('data-size');

                if (size > 0) {

                    // get corresponding video and pass to changePlayerSize
                    var $player = $(this).closest('.video-player').find('.video-js');
                    if ($player != undefined) {
                        if ($player?.prop("tagName") === "video" || helperFunctions.isIE8()) {
                            PlayerWidget.changePlayerSize($player, size);
                        } else {
                            $player = $player.find('video');
                            if ($player != undefined && $player.length > 0) {
                                PlayerWidget.changePlayerSize($player, size);
                            }
                        }
                    }

                    e.stopPropagation();
                    return false;
                }
            });
        },

        // sets the players dimension to small, medium, large, or xlarge
        changePlayerSize: function ($player, size) {

            if (helperFunctions.isIE8()) {
                // have to set both width, and height based on aspect ratio
                var newWidth = $player.parent().width() * (.01 * size);
                $player.width(newWidth).height(newWidth * PlayerWidget.aspectRatio);
            } else {
                // change player wrapper size
                $player.parent().css('width', size + '%');
            }
        },

        // sets player dimension based on aspect ratio
        resizeVideoJS: function (player) {

            var width = $('#' + player.id()).parent().width();  // don't include element padding
            player.width(width).height(width * PlayerWidget.aspectRatio);
        },

        // create span icons for new play button
        createPlayIcon: function (player) {

            //ex: ///player.autoplay(true);
        },

        init: function () {

            PlayerWidget.setGlobalPlayerSettings();
            PlayerWidget.bindPlayers();
        }
    };

    PlayerWidget.init();
});;
class TableFilters {
    #alphabet = "abcdefghijklmnopqrstuvwxyz".toUpperCase().split('');

    #alphaTemplate = `
<div class="filter-by-container alpha-filter-container" data-module="tables">
    <div class="filter-wrapper alpha-filter">
        <div class="filter-label">
            <span>FILTER BY:</span>
            <br>
        </div>
        <div class="alphabet-list">
            <ul></ul>
        </div>
    </div>
</div>`;

    #searchTemplate = `
<div class="half-sz form-section" style="margin-bottom: 10px;">
    <label>Search <a class="label-icon icomoon icon-Help2 hidden-xs" {{#if hasNoHelp}} style="display: none;" {{/if}}></a></label>
    {{{help}}}
    <input type="text" class="half-search" aria-label="search term">
    <input type="image" class="half-search-icon" src="/Presentation/DotGov/includes/images/permit/icon_magnify.png" aria-label="search submit">
</div>
<div class="clearfix"></div>`;

    #selectTemplate = `
<div class="form-section half-sz">
    <label>{{filter.Title}} <a class="label-icon icomoon icon-Help2 hidden-xs" {{#if hasNoHelp}} style="display: none;" {{/if}}></a></label>
    {{{help}}}
    <select class="half-select" aria-label="select"></select>
</div>`;

    #tagTemplate = `
<a class="keyword-filter-btn" role="button">
    <div class="filter-word">{{Label}}</div>
    <div class="filter-close icomoon icon-Close2"></div>
</a>`;

    #dateRangeTemplate = `
<div class="form-section" style="width: 100%;">
    <label>{{dateFilterHeader.DateRangeFilterTitle}} <a class="label-icon icomoon icon-Help2 hidden-xs" {{#if hasNoHelp}} style="display: none;" {{/if}}></a></label>
    {{{help}}}
    <div class="filter-date-range">
        <input id="data-input-from" type="text" name="start" placeholder="From" aria-label="date from" readonly />
    </div>
    
    <div class="filter-date-range">
        <input id="data-input-to" type="text" name="end" placeholder="To" aria-label="date to" readonly />
    </div>
    <div class="date-range-picker" style="display: none;">
        <div class="picker start-dp">
            <h6 class="text-center bold">From</h6>
        </div>
        <div class="picker end-dp">
            <h6 class="text-center bold">To</h6>
        </div>
        <div class="clearfix"></div>
        <div class="buttons">
            <a class="apply-filters close-picker" role="button">Close</a>
            <a class="apply-filters apply-picker" role="button">Apply</a>
        </div>
    </div>
</div>`;

    #grid;
    #$output;
    #$tagsContainer;
    #filterParams = {};
    #filterClearHandlers = {};
    #dataContext;
    #$noticeArea;
    #refreshTableFunc;
    #momentDisplayFormat = "mm-DD-YYYY";
    #momentSystemFormat = "mm-DD-YYYY";
    #helpTipManager;

    getFilters() {
        return this.#filterParams;
    }

    constructor(grid, $areaContainer, dataContext, dataUrl, refreshTableFunc, helpTipManager) {
        this.#dataContext = dataContext;
        this.#grid = grid;
        this.#helpTipManager = helpTipManager;

        this.#$output = $areaContainer;
        this.#refreshTableFunc = refreshTableFunc;
        this.#$tagsContainer = $areaContainer.find(".filter-tags").first();
        this.#$noticeArea = $areaContainer.find(".filter-notice").first();
        this.#$output.find(".permit-table-clear-filters").click(evt => {
            Object.values(this.#filterClearHandlers).forEach(val => {
                val();
            });
            if (Object.keys(this.#filterParams).length) {
                this.#filterParams = {};
            }
            this.#refresh();
        });
        this.#initFilterAreaState();

        const $filtersContainer = this.#$output.find(".filters-container");
        $.get(dataUrl)
            .done(data => {
                if (data) {
                    this.#initAlphabeticalFilter($filtersContainer);
                    this.#initializeSelects(data, $filtersContainer);
                    this.#initDateRangeFilter($filtersContainer);
                    this.#initSearch($filtersContainer);
                }
            });
    }


    tableUpdated() {
        if (this.#filterParams.search) {
            const sVal = this.#filterParams.search?.trim();
            if (sVal?.length) {
                for (const el of this.#dataContext.$table.find("td").toArray()) {
                    if (el.innerHTML.toLowerCase().indexOf(sVal.toLowerCase()) >= 0) {
                        this.#replaceTextBySearchTerm(sVal, el);
                    }
                }
            }
        }
    }

    #replaceTextBySearchTerm(sVal, el) {
        for (const child of $(el).children().toArray()) {
            const $child = $(child);
            if ($child.children().length) {
                this.#replaceTextBySearchTerm(sVal, child);
            } else {
                const text = $child.text();
                const firstIdx = text.toLowerCase().indexOf(sVal.toLowerCase());
                if (firstIdx >= 0) {
                    const regExVal = new RegExp(sVal, "ig");
                    const replacedText = text.replaceAll(regExVal, "<span class='keyword-filter'>" + text.substring(firstIdx, firstIdx + regExVal.source.length) + "</span>");
                    $child.html(replacedText);
                }
            }
        }
    }

    #initDateRangeFilter($filtersContainer) {
        const dateFilterHeader = this.#dataContext.headers.find(x => x.UseForDateRangeFilter);
        if (dateFilterHeader) {
            const $filter = this.#compileWithHelp(this.#dateRangeTemplate, dateFilterHeader.FilterHelpIconForPopup, {dateFilterHeader});
            const $picker = $filter.find(".date-range-picker");
            const $startPicker = $picker.find(".start-dp");
            const $endPicker = $picker.find(".end-dp");
            const $start = $filter.find("input[name=start]");
            const $end = $filter.find("input[name=end]");
            const dpSettings = {
                language: "en",
                dateFormat: "mm-dd-yyyy",  
                minView: "days", 
                view: "days",
                clearButton: true,
                inline: true
            };
            const startPicker = () => $startPicker.datepicker().data("datepicker");
            const endPicker = () => $endPicker.datepicker().data("datepicker");
            const nextMonth = moment().add(1, 'months').toDate();
            let startValPrev, endValPrev;
            $filter.find("input[name]").click(evt => {
                $picker.fadeIn(50);
                startValPrev = $start.val();
                endValPrev = endPicker().selectDate(nextMonth);
            });
            $startPicker.datepicker({
                ...dpSettings,
                onSelect: function onSelect(fd, date, picker) {
                    $start.val(fd);
                    endPicker().update({minDate: date});
                    if (endPicker().selectedDates.length && endPicker().selectedDates[0] < date) {
                        endPicker().clear();
                    }
                }
            });
            $endPicker.datepicker({
                ...dpSettings,
                onSelect: function onSelect(fd, date, picker) {
                    $end.val(fd);
                }
            });
            $picker.find("a.close-picker").click(evt => {
                if (startValPrev?.length) {
                    startPicker().selectDate(moment(startValPrev, this.#momentDisplayFormat).toDate());
                }
                else {
                    startPicker().clear();
                }
                if (endValPrev?.length) {
                    endPicker().selectDate(moment(endValPrev, this.#momentDisplayFormat).toDate());
                }
                else {
                    endPicker().clear();
                }
                $picker.fadeOut(50);
            });
            $picker.find("a.apply-picker").click(evt => {
                $picker.fadeOut(50);
                const startVal = $start.val();
                if (startVal?.length) {
                    this.#filterParams.dateFrom = moment(startVal, this.#momentDisplayFormat).format(this.#momentSystemFormat);
                } else
                    delete this.#filterParams.dateFrom;
                const endVal = $end.val();
                if (endVal?.length) {
                    this.#filterParams.dateTo = moment(endVal, this.#momentDisplayFormat).format(this.#momentSystemFormat);
                } else
                    delete this.#filterParams.dateTo;
                this.#refresh();
            });
            this.#filterClearHandlers.dateFrom = () => {
                startPicker().clear();
                delete this.#filterParams["dateFrom"];
                this.#filterClearHandlers.dateTo();
            };
            this.#filterClearHandlers.dateTo = () => {
                endPicker().clear();
                delete this.#filterParams["dateTo"];
            };
            $filtersContainer.prepend($filter);
        }
    }

    #initAlphabeticalFilter($filtersContainer) {
        if (!this.#dataContext.renderingParams.EnableAlphabeticalFiltering || !this.#dataContext.renderingParams.AlphabeticalFilteringByField) return;
        const $filter = $(this.#alphaTemplate);
        const $azList = $filter.find(".alphabet-list ul");
        const key = "alpha_" + this.#dataContext.renderingParams.AlphabeticalFilteringByField;
        for (const ch of this.#alphabet) {
            $azList.append($(`<li><a>${ch}</a></li>`));
        }
        $azList.find("li > a").click(evt => {
            this.#filterParams[key] = $(evt.currentTarget).text();
            this.#refresh();
        });
        this.#filterClearHandlers[key] = () => {
            delete this.#filterParams[key];
        };
        $filtersContainer.prepend($filter);
    }

    #initFilterAreaState() {
        const $collapseButton = this.#$output.find(".collapseFilterButton");
        $collapseButton.click(evt => {
            $collapseButton.toggleClass("collapsed");
            this.#$output.find("tr.collapse").toggleClass("in");
        });
        if (this.#dataContext.renderingParams.AutoExpandFilters) {
            $collapseButton.click();
        }
    }

    #compileWithHelp(template, helpObj, compileObj) {
        const help = this.#helpTipManager.compile(helpObj);
        const $filter = $(Handlebars.compile(template)(
            {
                ...compileObj,
                hasNoHelp: !help || help.length === 0,
                help
            }));
        this.#helpTipManager.bind($filter.find(".expand-popup"), $filter.find("a.label-icon"));
        return $filter;
    }

    #initializeSelects(data, $filtersContainer) {
        for (const filter of data.reverse()) {
            const helpObj = this.#dataContext.headers.find(x => x.ItemTrimmedFieldName === filter.ItemFieldName)?.FilterHelpIconForPopup;
            const $filter = this.#compileWithHelp(this.#selectTemplate, helpObj, {filter});
            const key = "filter_" + filter.ItemFieldName;
            const $select = $filter.find("select");
            $select.append($(`<option>${filter.EmptyText ? filter.EmptyText : ''}</option>`));
            for (const val of filter.Values) {
                const $opt = $(`<option value="${val.Key}">${val.Value}</option>`);
                $select.append($opt);
                const notice = filter.NoticesByValues[val.Key];
                if (notice?.length) {
                    $opt.data("notice", notice);
                }
            }
            $select.change(evt => {
                const val = $(evt.currentTarget).val();
                if (val?.length) {
                    this.#filterParams[key] = val;
                } else {
                    this.#filterClearHandlers[key]();
                }

                this.#refresh();
                const notice = $(evt.currentTarget).find(":selected").data("notice");
                if (notice) {
                    this.#$noticeArea.find(".notice").html(notice);
                    this.#$noticeArea.show();
                }
            });
            this.#filterClearHandlers[key] = () => {
                $select.val("");
                delete this.#filterParams[key];
            };
            $filtersContainer.prepend($filter);
        }
    }

    #initSearch($filtersContainer) {
        if (!this.#dataContext.renderingParams.EnableGlobalSearch) {
            return;
        }
        const helpObj = this.#dataContext.renderingParams.GlobalSearchHelp;
        const $search = this.#compileWithHelp(this.#searchTemplate, helpObj, {});
        const $searchInput = $search.find(".half-search");
        const $searchBtn = $search.find(".half-search-icon");
        $searchInput.keyup(evt => {
            if (evt.keyCode === 13) {
                $searchBtn.click();
            }
        });
        $searchBtn.click(evt => {
            const val = $searchInput.val();
            if (val?.length) {
                this.#filterParams.search = val;
            } else {
                this.#filterClearHandlers.search();
            }
            this.#refresh();
        });
        this.#filterClearHandlers.search = () => {
            $searchInput.val("");
            delete this.#filterParams["search"];
        };
        $filtersContainer.prepend($search);
    }

    #updateTagsArea() {
        const $wrapper = this.#$tagsContainer.find(".tags-wrapper");
        $wrapper.empty();
        if (!Object.keys(this.#filterParams).length) {
            this.#$tagsContainer.hide();
        } else {
            for (const p in this.#filterParams) {
                let label = this.#filterParams[p];
                if (p === "dateFrom") {
                    label = this.#formatDateTag(label);
                    if (this.#filterParams.dateTo) {
                        label += " to " + this.#formatDateTag(this.#filterParams.dateTo);
                    }
                } else if (p === "dateTo") {
                    if (this.#filterParams["dateFrom"]) continue;
                    label = "To " + this.#formatDateTag(label);
                } else {
                    label = label.split("|")[0];
                }

                const $tag = $(Handlebars.compile(this.#tagTemplate)({Label: label}));
                $tag.click(evt => {
                    this.#filterClearHandlers[p]();
                    this.#refresh();
                });
                $wrapper.append($tag);
            }
            this.#$tagsContainer.show();
        }
    }

    #formatDateTag(tag) {
        return moment(tag, this.#momentSystemFormat).format(this.#momentDisplayFormat);
    }

    #refresh() {
        let query = "";
        for (const p in this.#filterParams) {
            if (query.length) {
                query += "&";
            }
            query += `${p}=${this.#filterParams[p]}`;
        }

        const server = this.#grid.config.server;
        const url = this.#grid.config.server.url.split("?")[0];
        server.url = query.length ? url + "?" + query : url;
        this.#grid.updateConfig({
            server: server
        });
        this.#refreshTableFunc();
        this.#updateTagsArea();
        this.#$noticeArea.hide();
    }
};
class TableHelpPopup {
    #localStoragePermDisabledKey = "tblCloseHelpPopup";
    #overlayClass = "table-tip-overlay";
    #dataContext;
    #currentIndex = 0;
    #$allPopups;
    #isClosed = true;
    #$openButton;

    constructor(dataContext) {
        this.#dataContext = dataContext;
        if (this.#isEnabled) {
            this.#$allPopups = $(dataContext.helpTipRenderer.render(dataContext.renderingParams.HelpPopupsToShow, dataContext.strings)).filter(".expand-popup");

            this.#$allPopups.find(".closeBtn").click(evt => this.close());
            this.#$allPopups.find(".perm-disable").change(function () {
                localStorage.setItem('tblCloseHelpPopup', this.checked ? 'true' : '');
            });
            this.#$allPopups.find(".previous-tip-btn:not(.disabled)").click(evt => {
                this.close();
                this.#currentIndex--;
                this.#open(true);
            });

            this.#$allPopups.find(".next-tip-btn:not(.disabled)").click(evt => {
                this.close();
                this.#currentIndex++;
                this.#open();
            });
        }
    }

    initialize() {
        if (this.#isEnabledAndHasHelp) {
            if (!this.#$openButton) {
                this.#$openButton = this.#dataContext.$wrapper.find("#showHelpPopup").removeClass("hidden").click(evt => {
                    evt.preventDefault();
                    this.#ensureOverlay();
                    this.#open();
                });
                if (!this.#permanentDisabled && !!this.#dataContext.renderingParams.HelpShowOnLoad) {
                    this.#open(false, true);
                }
            } else {
                this.reOpen();
            }
        }
    }

    reOpen() {
        if (!this.#isClosed) {
            this.#open();
        }
    }

    get #isEnabled() {
        return this.#dataContext.renderingParams.EnableHelp;
    }

    get #isEnabledAndHasHelp() {
        return this.#isEnabled && this.#$allPopups?.length > 0;
    }

    #open(backward = false, doNotScroll = false) {
        for (let i = 0; i < this.#$allPopups.length; i++) {
            if (this.#show(doNotScroll)) return;
            if (backward) this.#currentIndex--;
            else this.#currentIndex++;

            if (this.#currentIndex >= this.#$allPopups.length) this.#currentIndex = 0;
            if (this.#currentIndex < 0) this.#currentIndex = this.#$allPopups.length - 1;
        }
    }

    #show(doNotScroll = false) {
        const $popup = this.#$popup;
        if (!$popup.length)
            return false;
        let targetParent;
        const customSelector = $popup.data("custom-selector");
        if (customSelector?.length) {
            targetParent = this.#dataContext.$wrapper.find(customSelector).first();
        } else {
            let helpRowNumber = $popup.data("help-row-number");
            if (helpRowNumber < 1) {
                helpRowNumber = 1;
            }

            let helpColNumber = $popup.data("help-col-number");
            if (helpColNumber < 1) {
                helpColNumber = 1;
            }

            targetParent = this.#dataContext.$table.find(`tbody:first > tr.rgRow:eq(${(helpRowNumber - 1)}) > td:eq(${(helpColNumber - 1)})`);
        }

        if (targetParent.length && targetParent.is(":visible")) {
            this.#dataContext.$wrapper.find(".expand-popup").hide();
            $popup.find(".perm-disable")[0].checked = this.#permanentDisabled;
            $popup.detach().appendTo(targetParent).show();
            if (!doNotScroll && $popup.is(":visible"))
                window.scrollTo({top: $popup[0].offsetTop, behavior: 'smooth'});
            this.#isClosed = false;
            return true;
        }
        return false;
    }

    close(temp = false) {
        if (this.#isEnabledAndHasHelp) {
            this.#$popup.detach();
        }
        if (!temp) this.#isClosed = true;
    }

    get #$popup() {
        return this.#$allPopups.eq(this.#currentIndex);
    }

    get #permanentDisabled() {
        return !!localStorage.getItem(this.#localStoragePermDisabledKey)?.length;
    }

    #ensureOverlay() {
        let $overlay = $("." + this.#overlayClass);
        if (!$overlay.length) {
            $overlay = $("<div>").addClass(this.#overlayClass);
        }
        $overlay.detach();
        $overlay.appendTo("body");
    }
};
class TableHelpTip {
    #dataContext;
    #helpPopupManager;
    #closeOutsideCss = "close-by-outside-click";
    
    constructor(dataContext, helpPopupManager) {
        this.#dataContext = dataContext;
        this.#helpPopupManager = helpPopupManager;
        $("body").click(evt =>
        {
            const selector = "." + this.#closeOutsideCss;
            if(!$(evt.target).closest(selector).length && !$(evt.target).is(selector) && !$(evt.target).is("a.label-icon")) {
                this.#hideAllHelp();
            }
        });
    }
    
    compile(helpObj) {
        return !!helpObj ? this.#dataContext.helpTipRenderer.render([helpObj], this.#dataContext.strings, false, true, this.#closeOutsideCss) : "";
    }
    
    bind($popup, $link) {
        if ($popup.length) {
            $link.click(evt => {
                this.#hideAllHelp();
                $popup.toggle();
                this.#helpPopupManager.close();
            });
        }
    }
    
    #hideAllHelp() {
        this.#dataContext.$wrapper.find("." + this.#closeOutsideCss).hide();
    }
}

class TableHelpPopupRenderer {
    #template = `
{{#*inline "LeanMoreLink"}}
    {{#if HelpModalPageId}}
        <a href="javascript:void(0);" data-toggle="modal" data-target="{{HelpModalPageId}}" class="white-link {{extraClass}}">{{{HelpLinkLabel}}}</a>
    {{else}}{{#if HelpLink}}
        <a href="{{HelpLink.Url}}" target="{{HelpLink.Target}}" class="white-link {{extraClass}}">{{{HelpLinkLabel}}}</a>
    {{/if}}{{/if}}
{{/inline}}

{{#each popups}}
    <div class="expand-popup point-{{this.PointerPosition.Name}} hidden-xs {{../customCssClass}}"
        style="margin-top: {{this.CustomTopMargin}}px; margin-left: {{this.CustomLeftMargin}}px; {{#if ../initiallyHidden}}display: none;{{/if}}"
        data-custom-selector="{{this.CustomCssSelector.Name}}"
        data-help-row-number="{{this.HelpPopupRowNumber}}"
        data-help-col-number="{{this.ColumnNumberToShowHelpPopup}}">
        <div class="hint-header">
            <h5>{{{this.HelpTitle}}}</h5>
            <a class="icon-Close icomoon closeBtn" title="{{{CloseButtonLabel}}}"
             {{#if ../initiallyHidden}} onclick="$(this).closest('.expand-popup').hide();"{{/if}}></a>
        </div>
        <div class="clear"></div>
        <div class="hint-text">
            {{{this.HelpDescription}}}
        </div>
        {{#if ../showStopCheckbox}}
        <div class="hint-check">
            <input class="custom-chckbx perm-disable" type="checkbox" value="">
            <span class="hint-lbl" for="noshow1">{{{this.StopShowingCheckboxLabel}}}</span>
        </div>
        <div class="space-5pxno"></div>
        {{/if}}
        <div class="full-width">
            {{#if ../hasManyPopups}}
                <div class="left-hint">
                    <a class="white-link flt-left previous-tip-btn {{#unless @index}}disabled{{/unless}}">
                        <div class="tt-btn-icon icomoon icon-ArrowLeft"></div>
                        <div class="tt-btn-text">{{{../strings.tableshelpprevtip}}}</div>
                    </a>
                    {{> LeanMoreLink extraClass="flt-left"}}
                    <div class="tip-text">{{{helpPopups_formatOneOfMany ../strings.tableshelpindextipofcount @index ../popups.length}}}</div>
                </div>
                <div class="right-hint">
                    <a class="white-link flt-right next-tip-btn {{helpPopups_disabledIfLast ../popups.length @index}}">
                        <div class="tt-btn-text">{{{../strings.tableshelpnexttip}}}</div>
                        <div class="tt-btn-icon icomoon icon-ArrowRight"></div>
                    </a>
                </div>
            {{else}}
                <div class="center-hint">
                    {{> LeanMoreLink extraClass="center-btn"}}
                </div>
            {{/if}}
        </div>
    </div>
{{/each}}`;

    constructor() {
        this.#registerTemplateHelpers();
    }

    render(popups, strings, showStopCheckbox = true, initiallyHidden = false, customCssClass = "") {
        return Handlebars.compile(this.#template)({
            popups,
            strings,
            hasManyPopups: popups.length > 1,
            showStopCheckbox,
            initiallyHidden,
            customCssClass
        });
    }

    #registerTemplateHelpers() {
        Handlebars.registerHelper("helpPopups_disabledIfLast", function (popups, index) {
            return index === popups - 1 ? "disabled" : "";
        });
        Handlebars.registerHelper("helpPopups_formatOneOfMany", function (str, index, length) {
            return str.replace("{0}", index + 1).replace("{1}", length);
        })
    }
};
class TableDataContext {
    constructor($wrapper, strings, renderingParams) {
        this.$wrapper = $wrapper;
        this.strings = strings;
        this.renderingParams = renderingParams;
    }

    $wrapper;
    #$table;
    #tableUpdated = $.Callbacks();
    strings;
    renderingParams;
    headers;
    headerStartIndex = 1;
    helpTipRenderer = new TableHelpPopupRenderer();

    get $table() {
        return this.#$table;
    }

    set $table(value) {
        this.#$table = value;
        this.#tableUpdated.fire(this.#$table);
    }

    tableInitialized(func) {
        this.#tableUpdated.add(func);
    }
}

class TableBlock {
    #paging;
    #sorting;
    #sitecoreItemId = "SystemRowId";
    #mobileViewCol = "TableMobileOnlyColumn";
    #sitecoreNestingDisabled = "SystemNestingDisabled";
    #altRowClass = "rgAltRow";
    #baseUrl = "/api/admin/table";
    #pageId;
    #dataSourceId;
    #renderingHash;
    #currentDataSet = [];
    #grid;
    #gridInitialized = false;
    #tableCaptionInitialized = false;
    #dataContext;
    #helpPopup;
    #helpTips;
    #autoExpandIds;
    #autoExpandScroll = false;
    tableUpdatedCallbacks = [];

    #captionAreaTemplate = `
<div>
    <table class="permit-table-header">
        <tbody>
            <tr class="permit-table-search">
                <td colspan="2">
                    <div class="h4">
                        {{#if hasFiltersOrSearch}}
                            <a class="collapsed collapseFilterButton" role="button" href="#">
                                <span class="caption-label">
                                {{#if hasSearch}}
                                    Search {{#if hasFilters}}&amp;{{/if}}
                                {{/if}}
                                {{#if hasFilters}}
                                    Filters
                                {{/if}}
                                </span> <span class="icon-caret"></span>
                                <span class="collapsed document-meta-data">{{renderingParams.HeaderHelpText}}</span>
                                <span class="expanded document-meta-data">{{renderingParams.CollapsedHeaderHelpText}}</span>
                            </a>
                        {{/if}}
                        {{#if renderingParams.ShowFeed}}
                            <a class="filter-help-btn" target="_blank" style="margin-left: 5px" href="{{feedUrl}}">
                                <div class="get-info-txt">Feed</div>
                            </a>
                        {{/if}}
                        <div class="buttons-container">
                        {{#if renderingParams.EnableHelp}}
                            <a class="filter-help-btn hidden" id="showHelpPopup" role="button" href="#">
                                <div class="icomoon get-info-icon icon-Help2"></div>
                                <div class="get-info-txt">{{{strings.tablesgethelpbuttonlabel}}}</div>
                            </a>
                        {{/if}}
                        {{#if renderingParams.ShowExport}}
                            <a id="export-csv-btn" class="filter-help-btn" style="margin-left: 5px" href="{{exportUrl}}" role="button" href="#">
                                <div class="get-info-txt">Download CSV</div>
                            </a>
                        {{/if}}
                        </div>
                        
                    </div>
                </td>
            </tr>
            {{#if hasFiltersOrSearch}}
                <tr class="permit-table-search permit-table-filters collapse">
                    <td colspan="2" style="display: inline-block; width: 100%;" class="filters-container">
                        <div class="clearfix"></div>
                        <p>
                            <button class="permit-table-clear-filters">
                            Clear
                            {{#if hasSearch}}
                                Search {{#if hasFilters}}&amp;{{/if}}
                            {{/if}}
                            {{#if hasFilters}}
                                Filters
                            {{/if}}
                            </button>
                        </p>
                        <div class="clearfix"></div>
                    </td>
                </tr>
            {{/if}}
        </tbody>
    </table>
    <div class="table-message tbl-msg4 color-2 filter-notice" style="display: none;">
        <table>
            <tbody>
            <tr>
                <td>
                    <div class="tbl-msg-icon icomoon icon-Asterisk"></div>
                </td>
                <td>
                    <div class="table-msg-txt notice">
                    </div>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
    {{#if renderingParams.TableHeaderDefinition}}
    {{#if renderingParams.TableHeaderDefinition.NoticeShow}}
        <div class="table-message color-1">
            <table>
                <tbody>
                <tr>
                    <td>
                        <div class="tbl-msg-icon icomoon {{renderingParams.TableHeaderDefinition.NoticeIcon}}"></div>
                    </td>
                    <td>
                        <div class="table-msg-txt">
                            {{{renderingParams.TableHeaderDefinition.NoticeBody}}}
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    {{/if}}
    {{/if}}
    {{#if hasFiltersOrSearch}}
        <div class="table-message color-4 filter-tags" style="display: none;">
            <table>
                <tbody>
                <tr>
                    <td>
                        <div class="tbl-msg-icon icomoon icon-SearchResults"></div>
                    </td>
                    <td>
                        <div class="table-msg-txt">
                            <span class="keyword-text">Below are the results of your search for:</span>
                            <span class="tags-wrapper"></span>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
             {{#if renderingParams.ShowExport}}
             <div id="export-filtered-csv-wrapper" style="display: none;">
                <a id="export-filtered-csv-btn" class="filter-help-btn" href="#" style="">
                    <div class="get-info-txt" style="">DOWNLOAD FILTERED CSV</div>
                </a>
            </div>
            {{/if}}
        </div>
       
    {{/if}}
</div>`;

    constructor(pageId, containerId, dataSourceId, renderingHash, renderingParams, strings, lang) {
        if (lang?.length) 
            this.#baseUrl = '/' + lang + this.#baseUrl;
        this.#dataContext = new TableDataContext($(`#${containerId}`), strings, renderingParams);
        this.#pageId = pageId;
        this.#dataSourceId = btoa(dataSourceId);
        this.#renderingHash = renderingHash;
        this.#helpPopup = new TableHelpPopup(this.#dataContext);
        this.#helpTips = new TableHelpTip(this.#dataContext, this.#helpPopup);

        $.get(`${this.#baseUrl}/headers/${this.#pageId}/${this.#renderingHash}${window.location.search}`)
            .done(data => {
                this.#dataContext.headers = data;
                const limit = this.#dataContext.renderingParams.ItemsPerPage ?? 10;
                $.get(`${this.#baseUrl}/autoexpand/${this.#pageId}/${this.#dataSourceId}/${this.#renderingHash}/${limit}${window.location.search}`)
                    .done(data => {
                        this.#autoExpandIds = data.AutoExpandRows;
                        this.#autoExpandScroll = data.AutoExpandScroll;
                        this.#initTable(limit, data.AutoExpandPage);
                    });
            });
        $(window).resize(() => {
            this.#switchToMobileViewIfNeeded();
        });
    }

    #initTable(limit, page) {
        const cols = [];
        const hasShowExport = this.#dataContext.renderingParams.ShowExport;
        cols.push({
            id: this.#sitecoreItemId,
            hidden: true
        });
        if (this.#hasNesting) {
            cols.push(new NestedColumn(this.#sitecoreItemId));
            this.#dataContext.headerStartIndex = 2;
        }

        for (const header of this.#dataContext.headers) {
            const col = {
                id: header.ItemTrimmedFieldName,
                name: gridjs.html(header.ImageSrc ? `<img src="${header.ImageSrc}" title="${header.Text ?? header.Title}">` : header.Title),
                formatter: (cell) => gridjs.html(cell),
                hidden: header.IsHiddenOrNested,
                targetField: header.TargetFieldName,
                rawView: header.RawDisplay,
                attributes: (cell, row) => {
                    if (row) {
                        const attrs = {
                            title: header.Tooltip
                        };
                        attrs[this.#sitecoreItemId] = row.cells[0].data;
                        return attrs;
                    }
                }
            };
            if (!header.AllowSorting) {
                col.sort = false;
            }
            if (header.Width && header.Width.length) {
                col.width = header.Width;
            }
            cols.push(col);
        }

        cols.push({
            id: this.#mobileViewCol,
            formatter: (cell) => gridjs.html(cell),
            attributes: {
                className: "table-mobile-only-column"
            }
        });

        this.#sorting = new TableSorting(this.#dataContext);
        this.#grid = this.#createGrid(cols);
        this.#paging = new TablePaging(this.#dataContext, this.#grid, limit, page, () => this.#refreshTable());
        this.#grid.on("beforeLoad", () => {
            if (this.#dataContext.$table) {
                TableUtils.makeFaded(this.#dataContext.$table);
            }
            this.#paging.adjustPagingVisibility(this.#isTableEmpty);
            this.#helpPopup.close(true);
        });

        this.#grid.on("ready", () => {
            setTimeout(() => {
                this.#dataContext.$table = this.#dataContext.$wrapper.find("table.rgMasterTable");
                this.#dataContext.$wrapper.fadeIn("fast");
                if (!this.#isTableEmpty) {
                    if (this.#sorting.manualSort(this.#gridInitialized) || this.#sorting.defaultSort(this.#gridInitialized)) {
                        return;
                    }
                    this.#adjustRows();
                    this.#sorting.handleSorting();
                    this.#initializeTableCaptionArea();
                    this.#renderNestedRows();
                    this.#autoExpand();
                    this.#switchToMobileViewIfNeeded();
                }
                this.#paging.init(this.#isTableEmpty);
                this.#paging.ensureItemsPerPageSelector();
                if (!this.#gridInitialized)
                    this.#helpPopup.initialize();
                else
                    this.#helpPopup.reOpen();
                this.#gridInitialized = true;
                for (const cb of this.tableUpdatedCallbacks) {
                    cb();
                }
                if (hasShowExport) {
                    document.getElementById('export-filtered-csv-wrapper').style.display = 'block'; //show csv button when table is loaded
                }
                TableUtils.makeVisible(this.#dataContext.$table);
            }, 100);
        });
        this.#grid.render(this.#dataContext.$wrapper.get(0));
    }

    #refreshTable() {
        const hasShowExport = this.#dataContext.renderingParams.ShowExport;
        this.#gridInitialized = false;
        if (hasShowExport) {
            document.getElementById('export-filtered-csv-wrapper').style.display = 'none'; //hide filter csv button when table is refreshed
        }
       
        this.#paging.load();
        this.#grid.forceRender();
    }

    #initializeTableCaptionArea() {
        if (this.#tableCaptionInitialized) {
            return;
        }
        const hasSearch = this.#dataContext.renderingParams.EnableGlobalSearch;
        const hasShowExport = this.#dataContext.renderingParams.ShowExport;
        
        const hasFilters =
            this.#dataContext.headers.some((x) => x.ShowInFilter) ||
            this.#dataContext.headers.some((x) => x.UseForDateRangeFilter) ||
            (this.#dataContext.renderingParams.EnableAlphabeticalFiltering && this.#dataContext.renderingParams.AlphabeticalFilteringByField);

        if (!this.#isTableEmpty && (hasFilters || hasSearch || this.#dataContext.renderingParams.EnableHelp || this.#dataContext.renderingParams.ShowFeed
            || this.#dataContext.renderingParams.ShowExport || this.#dataContext.renderingParams.TableHeaderDefinition?.NoticeShow)) {
            const $captionArea = $(Handlebars.compile(this.#captionAreaTemplate)({
                ...this.#dataContext,
                hasFilters: hasFilters,
                hasSearch: hasSearch,
                hasFiltersOrSearch: hasSearch || hasFilters,
                feedUrl: `${this.#baseUrl}/feed/${this.#pageId}/${this.#dataSourceId}/${this.#renderingHash}${window.location.search}`,
                exportUrl: `/admin/tableutils/CsvExportUnfiltered?pageId=${this.#pageId}&dataSourceId=${this.#dataSourceId}&renderingParamsHash=${this.#renderingHash}`
            }));
            this.#dataContext.$wrapper.prepend($captionArea);
            if (hasFilters || hasSearch) {
                const f = new TableFilters(this.#grid, $captionArea, this.#dataContext,
                    `${this.#baseUrl}/filters/${this.#pageId}/${this.#dataSourceId}/${this.#renderingHash}${window.location.search}`,
                    () => this.#refreshTable(), this.#helpTips);
                this.tableUpdatedCallbacks.push(() => {
                    const filterParams = f.getFilters();
                    const filteredBtn = document.getElementById('export-filtered-csv-btn');
                    /* Logic to display a download filtered csv button if table component already has a download csv option (hasShowExport)*/
                    if (hasShowExport && filterParams) {
                        const entries = Object.entries(filterParams);
                        if (entries.length > 0) {
                            const urlString = '&' + Object.entries(filterParams)
                                .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
                                .join('&');
                            filteredBtn.href = `/admin/tableutils/CsvExport?pageId=${this.#pageId}&dataSourceId=${this.#dataSourceId}&renderingParamsHash=${this.#renderingHash}${urlString}`;
                        }
                    }
                    f.tableUpdated();
                });
            }
        }
        this.#tableCaptionInitialized = true;
    }

    #createGrid(cols) {
        return new gridjs.Grid({
            columns: cols,
            className: {
                th: "rgHeader",
                tr: "rgRow",
                table: "rgMasterTable",
                container: "RadGrid RadGrid_Default",
                pagination: "rgPager",
                paginationButtonPrev: "rgPagePrev",
                paginationButtonNext: "rgPageNext",
                paginationSummary: "rgWrap rgInfoPart",
                paginationButtonCurrent: "rgCurrentPage"
            },
            sort: this.#sorting.defaultSettings,
            autoWidth: true,
            language: {
                pagination: {
                    previous: '◄',
                    next: '►',
                    showing: " ",
                    of: " ",
                    to: " ",
                    results: "items",
                    page: (page) => "",
                    navigate: (page, pages) => {
                        this.#paging.currentPage = page;
                        this.#paging.totalPages = pages;
                        return `Page ${page} of ${pages}`;
                    }
                },
                noRecordsFound: this.#dataContext.renderingParams.EmptyDataMessage
            },
            server: {
                url: `${this.#baseUrl}/data/${this.#pageId}/${this.#dataSourceId}/${this.#renderingHash}${window.location.search}`,
                then: data => this.#processDataResponse(data, cols),
                total: data => data.Count
            }
        });
    }

    #processDataResponse(data, cols) {
        if (!data.Data) {
            this.#currentDataSet = [];
            return null;
        }
        this.#currentDataSet = data.Data;
        return data.Data.map(row => {
            const result = [];
            for (const c of cols) {
                let val = Object.hasOwn(row, c.id) ? row[c.id] : row[c.targetField];
                result.push(!!c.rawView ? val : TableUtils.tryFormatDateOrNA(val));
            }
            return result;
        });
    }

    #adjustRows() {
        let counter = 0;
        for (const row of this.#dataContext.$table.find("tr.rgRow").toArray()) {
            const $row = $(row);
            const id = $row.find(`td[${this.#sitecoreItemId}]`).first().attr(this.#sitecoreItemId);
            $row.attr(this.#sitecoreItemId, id);
            if (counter++ % 2 === 0) {
                $row.addClass(this.#altRowClass);
            }
        }
        this.#dataContext.$table.find(".gridjs-td").removeClass("gridjs-td");
    }

    #renderNestedRows() {
        if (!this.#hasNesting) {
            return;
        }

        this.#dataContext.$table.find("tr.nested-row").remove();
        for (const row of this.#currentDataSet) {
            const id = row[this.#sitecoreItemId];
            const $targetRow = this.#dataContext.$table.find(`tr[${this.#sitecoreItemId}='${id}']`).first();
            if (!this.#dataContext.renderingParams.HideNestingForCancelledItems || !row[this.#sitecoreNestingDisabled]) {
                const $nestedRow = new NestedRow(this.#sitecoreItemId, this.#dataContext.headers, row, this.#helpTips);
                $nestedRow.insertAfter($targetRow);
                if ($targetRow.hasClass(this.#altRowClass)) {
                    $nestedRow.addClass(this.#altRowClass);
                }
            } else if (this.#dataContext.renderingParams.HideNestingForCancelledItems) {
                $targetRow.find("td.rgExpandCol").addClass("nestingDisabled");
            }
        }
    }

    get #hasNesting() {
        return this.#dataContext.renderingParams.EnableNesting && this.#dataContext.headers.some((x) => x.IsNested);
    }

    #autoExpand() {
        const certainAutoExpand = !!this.#autoExpandIds?.length;
        if (this.#dataContext.renderingParams.NestedAutoExpandOptions === "Auto Expand All Rows" && !certainAutoExpand) {
            this.#dataContext.$table.find(".col-header-expand").click();
            return;
        }

        if (!this.#gridInitialized && certainAutoExpand) {
            for (const id of this.#autoExpandIds) {
                this.#dataContext.$table.find(`tr[${this.#sitecoreItemId}='${id}']:first .rgExpand`).click();
            }

            if (this.#autoExpandScroll) {
                const targetPos = this.#dataContext.$table.find(`tr[${this.#sitecoreItemId}='${this.#autoExpandIds[0]}']:first`).offset();
                if (targetPos)
                    $("html,body").animate({
                        scrollTop: targetPos.top - 25
                    }, 1000);
            }
            this.#autoExpandScroll = false;
            this.#autoExpandIds = [];
        }
    }

    #switchToMobileViewIfNeeded() {
        if (this.#dataContext.$wrapper.find(".table-mobile-only-column").is(":visible")) {
            //$('.RadGrid_Default thead').hide();
            this.#dataContext.$wrapper.find('.RadGrid_Default thead tr').not('.rgPager').hide();
            this.#dataContext.$wrapper.find('.RadGrid_Default tbody tr td').not('.table-mobile-only-column').hide();
        } else {
            this.#dataContext.$wrapper.find('.RadGrid_Default tbody tr td').not('.table-mobile-only-column').show();
            //$('.RadGrid_Default thead').show();
            this.#dataContext.$wrapper.find('.RadGrid_Default thead tr').not('.rgPager').show();
        }
    }

    get #isTableEmpty() {
        return !this.#currentDataSet || !this.#currentDataSet.length;
    }
};
class NestedColumn {
    #sitecoreItemId;
    #expandAll = null;

    constructor(sitecoreItemIdConst) {
        this.#sitecoreItemId = sitecoreItemIdConst;
        return {
            id: "expand_collapse",
            name: gridjs.h("input", {
                type: "button",
                className: "col-header-expand",
                ariaLabel: "expand",
                onClick: evt => this.#expandAllAction(evt)
            }),
            formatter: (cell, row) => {
                return gridjs.h("input", {
                    type: "button",
                    className: "rgExpand",
                    ariaLabel: "expand",
                    onClick: evt => this.#expandAction(evt)
                });
            },
            attributes: {
                className: "rgHeader rgExpandCol"
            },
            sort: false,
            width: "44px"
        };
    }

    #expandAllAction(evt) {
        const $this = $(evt.currentTarget);
        this.#expandAll = $this.hasClass("col-header-expand");
        $this.closest("table").find("td.rgExpandCol input").click();
        $this.toggleClass("col-header-expand");
        $this.toggleClass("col-header-collapse");
        this.#expandAll = null;
    }

    #expandAction(evt) {
        const $this = $(evt.currentTarget);
        const id = $this.closest("tr").attr(this.#sitecoreItemId);
        const $nestedRow = $this.closest("tbody").find(`tr.nested-row[${this.#sitecoreItemId}='${id}']`);
        if (this.#expandAll == null) {
            $nestedRow.toggle();
            $this.toggleClass("rgExpand");
            $this.toggleClass("rgCollapse");
        } else {
            $nestedRow.toggle(this.#expandAll);
            $this.toggleClass("rgExpand", !this.#expandAll);
            $this.toggleClass("rgCollapse", this.#expandAll);
        }
    }
};
class NestedRow {
    #helpTipManager;
    #nestedRowTemplate =
        `<tr style="display: none;" class="nested-row">
            <td class="rgExpandCol">&nbsp;</td>
            <td colspan="1">
                <div class="nested-view">
                    <div class="content">
                        <div class="col-sm-4 padding-left-0 col1"></div>
                        <div class="col-sm-4 padding-left-0 col2"></div>
                        <div class="col-sm-4 padding-left-0 col3"></div>
                        <div class="padding-left-0 single-row" style="float: left; width: 100%;"></div>
                    </div>
                </div>
            </td>
        </tr>`;

    constructor(sitecoreItemIdConst, headers, row, helpTipManager) {
        this.#helpTipManager = helpTipManager;
        const $nestedRow = $(this.#nestedRowTemplate);
        for (const header of headers.filter((x) => x.IsNested)) {
            let value = row[header.ItemTrimmedFieldName];
            if (value === "$hideintable$") {
                continue;
            }
            value = TableUtils.tryFormatDate(value);
            const $dataHeader = $(`<h3>${header.Title}</h3>`);
            const $dataContent =  $(`<div class="field-content">${value}</div>`);
            if (!!header.HelpIconForPopup) {
                const $help = $(helpTipManager.compile(header.HelpIconForPopup));
                const $icon = $(`<a class="label-icon icomoon icon-Help2 hidden-xs"></a>`);
                $dataHeader.append($icon).append($help);
                helpTipManager.bind($help, $icon);
            }
            
            switch (header.NestedSectionLocation.toLowerCase()) {
                case "single row":
                    $nestedRow.find("div.single-row").append($dataHeader).append($dataContent);
                    break;
                case "column 2":
                    $nestedRow.find("div.col2").append($dataHeader).append($dataContent);
                    break;
                case "column 3":
                    $nestedRow.find("div.col3").append($dataHeader).append($dataContent);
                    break;
                default:
                    $nestedRow.find("div.col1").append($dataHeader).append($dataContent);
            }
        }

        $nestedRow.find("td[colspan]").attr("colspan", headers.filter((x) => !x.IsHiddenOrNested).length);
        $nestedRow.attr(sitecoreItemIdConst, row[sitecoreItemIdConst]);
        return $nestedRow;
    }
};
class TablePaging {
    #pagingAmountSelectTemplate = `
<div class="rgWrap rgAdvPart items-select">
    <span class="rgPagerLabel">Items per Page:</span>
    <select aria-label="items per page">
        {{#each items}}
            {{#if this.selected}}
            <option selected>{{this.value}}</option>
            {{else}}
            <option>{{this.value}}</option>
            {{/if}}
        {{/each}}
    </select>
</div>`;

    #predefinedItemsPerPageSelect = [10, 20, 50];
    #dataContext;
    #grid;
    #visible = false;
    #refreshTableFunc;
    #currentPage = 0;
    #totalPages = 0;
    #$topPager;

    constructor(dataContext, grid, limit, initialPage, refreshTableFunc) {
        this.#dataContext = dataContext;
        this.#grid = grid;
        this.#refreshTableFunc = refreshTableFunc;
        this.load(limit, initialPage);
        if (!this.#predefinedItemsPerPageSelect.includes(limit)) {
            this.#predefinedItemsPerPageSelect.push(limit);
            this.#predefinedItemsPerPageSelect.sort((a, b) => a - b);
        }
        if (this.#dataContext.renderingParams.PagingTop && !this.#dataContext.renderingParams.PagingBottom) {
            this.#paginationPlugin.position = gridjs.PluginPosition.Header;
        }
    }

    load(limit, page) {
        this.#grid.updateConfig({
            pagination: this.#getPaginationSettings(limit, page)
        });
    }

    ensureItemsPerPageSelector() {
        if (this.#pagingEnabled && !this.#$pager.find(".items-select").length) {
            const finalItems = [];
            const currentLimit = parseInt(this.#paginationPlugin.props.limit);
            for (const item of this.#predefinedItemsPerPageSelect) {
                const finalItem = {value: item, selected: item === currentLimit};
                finalItems.push(finalItem);
            }
            const $pageSelector = $(Handlebars.compile(this.#pagingAmountSelectTemplate)({
                items: finalItems
            }));
            $pageSelector.find("select").change(evt => {
                this.#grid.updateConfig({
                    pagination: this.#getPaginationSettings(parseInt(evt.currentTarget.value))
                });
                this.#refreshTableFunc();
            });
            this.#$pager.append($pageSelector);
        }
    }

    adjustPagingVisibility(isTableEmpty) {
        if (!this.#pagingEnabled) {
            return;
        }

        const $pagerButtons = this.#$pager.find(".gridjs-pages");
        this.#visible = !isTableEmpty && this.#totalPages > 1;
        $pagerButtons.toggle(this.#visible);
    }

    init(isTableEmpty) {
        this.adjustPagingVisibility(isTableEmpty);
        const $pagerButtons = this.#$pager.find(".gridjs-pages");
        $pagerButtons.find("button").each((i, el) => {
            const $el = $(el);
            const textAsNum = Number.parseInt($el.text());
            const page = !Number.isNaN(textAsNum) ? $el.text() :
                ($el.hasClass("rgPagePrev") ? "prev" : 
                    ($el.hasClass("rgPageNext") ? "next" : null));
            if (page) $el.attr("page", page);
            if (page === "prev") $el.attr("title", "Previous Page");
            if (page === "next") $el.attr("title", "Next Page");
        });
        const getButtonByPage = (page) => $pagerButtons.find(`button[page=${page}]`);
        if ($pagerButtons.find(".rgPageFirst").length === 0) {
            const $firstPage = $(`<button role="button" title="First Page" class="rgPageFirst"><b>◄|</b></button>`).click(evt => {
                if (this.#currentPage !== 1) getButtonByPage(1).click();
            });
            $pagerButtons.prepend($firstPage);
        }

        if ($pagerButtons.find(".rgPageLast").length === 0) {
            const $lastPage = $(`<button role="button" title="Last Page" class="rgPageLast"><b>|►</b></button>`).click(evt => {
                if (this.#currentPage !== this.#totalPages) getButtonByPage(this.#totalPages).click();
            });
            $pagerButtons.append($lastPage);
        }
        const $info = this.#$pager.find(".rgInfoPart");
        if (!$info.find("span").length) {
            $info.append(`<span> in <b>${this.#totalPages}</b> page${this.#totalPages !== 1 ? 's' : ''}</span>`);
        }
        
        if (this.#dataContext.renderingParams.PagingTop && this.#dataContext.renderingParams.PagingBottom) {
            if (this.#$topPager) {
                this.#$topPager.remove();
            }
            this.#$topPager = this.#$pager.parent().clone(true, true);
            this.#$topPager.removeClass().addClass("gridjs-head");
            this.#$topPager.find(".gridjs-pages button[page]").click(evt => getButtonByPage($(evt.currentTarget).attr("page")).click());
            this.#$topPager.insertBefore(this.#dataContext.$wrapper.find(".gridjs-wrapper"));
        }
    }

    set currentPage(val) {
        this.#currentPage = val;
    }

    set totalPages(val) {
        this.#totalPages = val;
    }

    #getPaginationSettings(limit, page) {
        return {
            enabled: this.#pagingEnabled,
            page: page ?? 0,
            limit: limit ?? this.#paginationPlugin.props.limit,
            resetPageOnUpdate: page === undefined,
            buttonsCount: 4,
            server: {
                url: (prev, page, limit) => {
                    return `${prev}${prev.includes('?') ? '&' : '?'}limit=${limit}&offset=${page * limit}`;
                }
            }
        };
    }

    get #pagingEnabled() {
        return this.#dataContext.renderingParams.EnablePaging;
    }

    get #paginationPlugin() {
        return this.#grid.config.plugin.get("pagination");
    }

    get #$pager() {
        return this.#dataContext.$wrapper.find(".rgPager");
    }
};
class TableSorting {
    #dataContext;
    #sortIsInProgress = null;
    #manuallySorted = false;
    #manualSortingColumn = null;
    #manualSortingDir = null;

    constructor(dataContext) {
        this.#dataContext = dataContext;
        this.#dataContext.tableInitialized($table => {
            $table.find(".gridjs-th-sort").click(evt => {
                if (!this.#sortIsInProgress) {
                    this.#manuallySorted = true;
                }
            });
        });
    }

    get defaultSettings() {
        return {
            enabled: this.#dataContext.renderingParams.EnableSorting,
            multiColumn: false,
            server: {
                url: (prev, columns) => {
                    return this.#getSortUrl(prev, columns);
                }
            }
        };
    }

    handleSorting() {
        setTimeout(() => {
            if (this.#manuallySorted) {
                this.#dataContext.$table.find("td").removeClass("rgSorted");
                this.#dataContext.$table.find(`td[data-column-id='${this.#manualSortingColumn}']`).addClass("rgSorted");
            }
        }, 100);
    }

    defaultSort(gridInitialized) {
        if (this.#dataContext.renderingParams.EnableSorting && !gridInitialized && !this.#manuallySorted) {
            const columnWithDefaultSort = this.#dataContext.headers.find(x => x.DefaultSortOrder && x.DefaultSortOrder.length);
            if (columnWithDefaultSort) {
                return this.#doSort(columnWithDefaultSort.ItemTrimmedFieldName, columnWithDefaultSort.DefaultSortOrder);
            }
        }
        return false;
    }

    manualSort(gridInitialized) {
        if (!gridInitialized && this.#manuallySorted) {
            return this.#doSort(this.#manualSortingColumn, this.#manualSortingDir);
        }
        return false;
    }

    #doSort(col, dir) {
        if (this.#sortIsInProgress !== 0) {
            const th = this.#dataContext.$table.find(`th.gridjs-th-sort[data-column-id=${col}]:first`);
            if (th.length) {
                if (this.#sortIsInProgress == null) {
                    this.#sortIsInProgress = dir === "Descending" || dir === "desc" ? 2 : 1;
                }
                th.click();
                this.#sortIsInProgress--;
                return true;
            }
        } else {
            this.#sortIsInProgress = null;
        }
        return false;
    }

    #getSortUrl(prev, columns) {
        if (!columns.length) return prev;
        const col = columns[0];
        this.#manualSortingDir = col.direction === 1 ? "asc" : "desc";
        this.#manualSortingColumn = this.#dataContext.headers[col.index - this.#dataContext.headerStartIndex].ItemTrimmedFieldName;
        this.handleSorting();
        return `${prev}${prev.includes('?') ? '&' : '?'}order=${this.#manualSortingColumn}&dir=${this.#manualSortingDir}`;
    }
};
class TableUtils {
    static tryFormatDate(value) {
        const date = this.#parseDate(value);
        return this.#isValidDate(date) ? date.locale("en").format("l") : value;
    }    
    
    static tryFormatDateOrNA(value) {
        return this.#isMinDate(this.#parseDate(value)) ? "<span class='not-applicable'>N/A</span>" : this.tryFormatDate(value);
    }

    static makeVisible($el) {
        return $el.css("visibility", "visible").css("opacity", "1");
    }

    static makeFaded($el) {
        return $el.css("opacity", "0.5");
    }
    
    static #isValidDate(momentDate) {
        return momentDate.isValid() && momentDate.year() !== 1;
    }

    static #isMinDate(momentDate) {
        return momentDate.isValid() && momentDate.year() === 1;
    }

    static #parseDate(value) {
        return this.isNumeric(value) ? moment("invalid date") : moment(value, moment.ISO_8601);
    }

    static isNumeric(str) {
        if (typeof str != "string") return false;
        return !isNaN(str) && !isNaN(parseFloat(str));
    }
};
class LiveStreamHelper {
    static ToggleHelpPopup(_this) {
        var $popup = $(_this).next();
        if ($popup.css("display") === "none") {
            $popup.css("display", "inline-block");
            LiveStreamHelper.SetOverflowPopup(_this);
        }
        else {
            $popup.hide();
            LiveStreamHelper.ResetOverflowPopup(_this);
        }
    }

    static ScrollToTopLanguages(_this) {
        var topPopup = document.querySelector('.language-picker .expand-popup.lang-select');
        topPopup.style.display = "inline-block";
        window.scrollTo({top: topPopup.offsetTop - 50, behavior: "smooth"});
        $(_this).closest(".expand-popup").hide();
    }

    static SwitchLang(_this, id) {
        LiveStreamHelper.CloseLangPopup(_this);
        var $target = $(`.btn-lang-area[data-livestream-id='${id}']`);
        $target.siblings().hide();
        $target.show();
    }
    
    static CloseLangPopup(_this) {
        $(_this).closest('.lang-select').hide();
        LiveStreamHelper.ResetOverflowPopup(_this);
    }

    static SetOverflowPopup(_this) {
        $(_this).closest('.chrt-tbl-area').css("overflow", "visible");
        $(_this).closest('.tab.flr-hdr.other').css("overflow", "visible");
        $(_this).closest('.tab.flr-hdr.other').css("z-index", "1000");
    }

    static ResetOverflowPopup(_this) {
        $(_this).closest('.chrt-tbl-area').css("overflow", "");
        $(_this).closest('.tab.flr-hdr.other').css("overflow", "");
        $(_this).closest('.tab.flr-hdr.other').css("z-index", "");
    }
};

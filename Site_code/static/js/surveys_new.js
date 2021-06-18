'use strict';
Array.prototype.insert = function (index, item) {
    if (index === 0)
        this.unshift(item);
    else
        this.splice(index, 0, item);
};

let ItemType = {
    OpenQuestion: {value: 1, name: "Open-ended Question"},
    ClosedQuestion: {value: 2, name: "Closed-ended Question"},
};

let OpenQuestionRegex = {
    Free: {name: "No restriction", regex: ""},
    UInt: {name: "Unsigned integer number", regex: "[1-9]+[0-9]*"},
    Int: {name: "Signed integer number", regex: "([\\+-]?[1-9]+[0-9]*)|(0)"},
    UDecimal: {name: "Unsigned Decimal number", regex: "(([1-9]+[0-9]*)|(0))(\\.([1-9]+[0-9]*)|\\.(0))?"},
    Decimal: {name: "Signed Decimal number", regex: "[\\+-]?(([1-9]+[0-9]*)|(0))(\\.([1-9]+[0-9]*)|\\.(0))?"},
    OneWord: {name: "Only one word", regex: "[a-zA-Z]+"},
    Alphanumerics: {name: "Only alphanumeric chars", regex: "[a-zA-Z0-9 ]+"},
};

class SurveysItem {
    constructor() {
        this.type = ItemType.OpenQuestion;
        this.addButton = new AddButton(this);

        this.$container = null;
        this.$body = null;
        this.$select_type = null;
        this.$btn_delete = null;
        this.$btn_up = null;
        this.$btn_down = null;
        this.$chk_mandatory = null;

        //Open
        this.$openType = null;
        this.$customRegexContainer = null;
        this.$customRegex = null;

        //Close
        this.$addButton = null;
        this.$tbody = null;
        this.$deleteButtons = null;

        this.draw();
        this.setEvents();
        this.$select_type.trigger('change');
    }

    draw() {
        let html = '';
        html += '<div class="card item-container">';
        html += '    <div class="card-header">';
        html += '        <div class="row justify-content-between">';
        html += '            <div class="col">';
        html += '                <input type="text" name="title" maxlength="150" required="" placeholder="Title" class="form-control">';
        html += '            </div>';
        html += '            <div class="col-auto">';
        html += '                <div class="btn-group">';
        html += '                    <button class="btn btn-danger item-cmd-delete" role="button">';
        html += '                        <i class="fas fa-trash-alt"></i>';
        html += '                    </button>';
        html += '                    <button class="btn btn-primary item-cmd-up" role="button">';
        html += '                        <i class="fas fa-chevron-up"></i>';
        html += '                    </button>';
        html += '                    <button class="btn btn-primary item-cmd-down" role="button">';
        html += '                        <i class="fas fa-chevron-down"></i>';
        html += '                    </button>';
        html += '                </div>';
        html += '            </div>';
        html += '        </div>';
        html += '    </div>';
        html += '    <div class="card-body">';
        html += '        <h5 class="card-title">Special title treatment</h5>';
        html += '        <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>';
        html += '       <a href="#" class="btn btn-primary">Go somewhere</a>';
        html += '   </div>';
        html += '   <div class="card-footer">';
        html += '       <div class="row justify-content-between">';
        html += '           <div class="col-auto ">';
        html += '               <select class="form-control mr-2 item-cmd-type">';
        for (let i in ItemType) {
            html += '               <option value="' + ItemType[i].value + '">' + ItemType[i].name + '</option>';
        }
        html += '               </select>';
        html += '           </div>';
        html += '           <div class="col-auto form-inline">';
        html += '               <label class="mr-2">Mandatory Question? </label>';
        html += '               <input class="item-mandatory" type="checkbox">';
        html += '           </div>';
        html += '       </div>';
        html += '   </div>';
        html += '</div>';
        this.$container = $(html);
        this.$body = this.$container.find('.card-body');
        this.$select_type = this.$container.find('.item-cmd-type');
        this.$btn_delete = this.$container.find('.item-cmd-delete');
        this.$btn_up = this.$container.find('.item-cmd-up');
        this.$btn_down = this.$container.find('.item-cmd-down');
        this.$chk_mandatory = this.$container.find('.item-mandatory');
        // this.$chk_mandatory.bootstrapToggle();
    }

    setEvents() {
        this.$select_type.off('change').change(this.type_change());
        this.$btn_delete.off('click').click(this.delete_click());
        this.$btn_up.off('click').click(this.up_click());
        this.$btn_down.off('click').click(this.down_click());
    }

    setButtonVisibility(index) {
        this.$btn_up.removeAttr('disabled');
        this.$btn_down.removeAttr('disabled');
        if (index === 0)
            this.$btn_up.attr('disabled', '');
        if (index === items.length - 1)
            this.$btn_down.attr('disabled', '');
    }

    insertAtIndex(index, $prev) {
        if (!$prev) {
            if (index === 0)
                $prev = topAddButton.$container;
            else
                $prev = items[index - 1].addButton.$container;
        }

        items.insert(index, this);
        this.$container.insertAfter($prev); //Insert items
        this.addButton.$container.insertAfter(this.$container); //Insert add button

        this.setEvents();
        this.addButton.setEvents();

        for (let i = 0; i < items.length; i++) {
            items[i].setButtonVisibility(i);
        }
    }

    remove() {
        this.$container.remove();
        this.addButton.remove();
        items.splice(items.indexOf(this), 1); //Remove item
    }

    type_change() {
        let that = this;
        return function () {
            let type = this.value;

            let html = '';
            if (type === "1") //Open-ended Question
            {
                html += '<div class="form-inline">';
                html += '   <label class="font-weight-bold pr-3">Select answer type:</label>';
                html += '   <select class="form-control item-openType">';
                for (let i in OpenQuestionRegex) {
                    html += '   <option value="' + OpenQuestionRegex[i].regex + '">' + OpenQuestionRegex[i].name + '</option>';
                }
                html += '       <option value="custom">Custom</optionval>';
                html += '   </select>';
                html += '</div>';
                html += '<div class="mt-2 item-customRegexContainer" hidden="hidden">';
                html += '   <div class="form-inline">';
                html += '       <label class="font-weight-bold pr-3">Insert custom Regex:</label>';
                html += '       <input class="form-control item-customRegex" type="text"/>';
                html += '   </div>';
                html += '   <div class="form-inline">';
                html += '       <label class="font-weight-bold pr-3">Insert Regex description:</label>';
                html += '       <input class="form-control item-customRegexDescription" type="text"/>';
                html += '   </div>';
                html += '</div>';

                that.$body.html(html);

                that.$openType = that.$body.find('.item-openType');
                that.$customRegexContainer = that.$body.find('.item-customRegexContainer');
                that.$customRegex = that.$body.find('.item-customRegex');
                that.$openType.off('change').change(function () {
                    if (this.value === "custom")
                        that.$customRegexContainer.removeAttr("hidden");
                    else
                        that.$customRegexContainer.attr("hidden", "hidden");
                });
            }
            else if (type === "2") //Closed-ended Question
            {
                let option = '';
                option += '    <tr>';
                option += '      <td><input type="text" class="form-control item-option"/></td>';
                option += '      <td><button class="btn btn-sm btn-danger item-cmd-removeOption" type="button"><i class="fas fa-times fa-fw"></i></button></td>';
                option += '    </tr>';

                html += '<table class="table table-striped table-bordered">';
                html += '  <thead>';
                html += '    <tr>';
                html += '      <th scope="col">Option</th>';
                html += '      <th scope="col"><button class="btn btn-sm btn-success item-cmd-insertOption" type="button"><i class="fas fa-plus fa-fw"></i></button></th>';
                html += '    </tr>';
                html += '  </thead>';
                html += '  <tbody>';
                html +=         option;
                html += '  </tbody>';
                html += '</table>';


                let deleteButtonsEvent = function (evt)
                {
                    $(evt.target).closest("tr").remove();
                };

                that.$body.html(html);
                that.$addButton = that.$body.find('.item-cmd-insertOption');
                that.$tbody = that.$body.find('tbody');

                that.$deleteButtons = that.$body.find('.item-cmd-removeOption');
                that.$deleteButtons.off('click').click(deleteButtonsEvent);
                that.$addButton.off('click').click(function (evt)
                {
                    that.$tbody.append(option);

                    that.$deleteButtons = that.$body.find('.item-cmd-removeOption');
                    that.$deleteButtons.off('click').click(deleteButtonsEvent);
                });
            }


        };
    }

    delete_click() {
        let that = this;
        return function () {
            that.remove();
        };
    }

    up_click() {
        let that = this;
        return function () {
            let currentIndex = items.indexOf(that);
            let newIndex = Math.max((currentIndex - 1), 0);

            that.remove();
            that.insertAtIndex(newIndex);
        };
    }

    down_click() {
        let that = this;
        return function () {
            let currentIndex = items.indexOf(that);
            let newIndex = Math.min((currentIndex + 1), items.length - 1);

            that.remove();
            that.insertAtIndex(newIndex);
        };
    }
}

class AddButton {
    constructor(after) {
        this.after = after;
        this.$container = null;
        this.$button = null;
        this.draw();
        this.setEvents();
    }

    draw() {
        let html = '';
        html += '<div class="row mt-3 mb-3">';
        html += '<div class="col">';
        html += '<hr>';
        html += '</div>';
        html += '<div class="col-auto btn-group">';
        html += '<button class="btn btn-success" role="button" data-toggle="tooltip" data-placement="top" title="" data-original-title="Add new item">';
        html += '<i class="fas fa-plus"></i>';
        html += '</button>';
        html += '</div>';
        html += '<div class="col">';
        html += '<hr>';
        html += '</div>';
        html += '</div>';

        this.$container = $(html);
        this.$button = this.$container.find(".btn");
    }

    setEvents() {
        this.$button.off('click').click(this.add_click())
    }

    add_click() {
        let that = this;
        return function () {
            let newItem = new SurveysItem();
            let newIndex = 0;
            if (that.after) {
                newIndex = items.indexOf(that.after) + 1;
            }
            newItem.insertAtIndex(newIndex, that.$container);
        };
    }

    remove() {
        this.$container.remove();
    }
}

let items = [];
let topAddButton = new AddButton(null);
$(function () {
    $('#itemsContainer').append(topAddButton.$container);
});
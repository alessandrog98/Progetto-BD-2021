'use strict';
Array.prototype.insert = function (index, item) {
    if(index === 0)
        this.unshift(item);
    else
        this.splice(index, 0, item);
};

let ItemType = {
    OpenQuestion : {value: 1, name: "Open-ended Question"},
    ClosedQuestion: {value: 2, name: "Closed-ended Question"},
};

class SurveysItem
{
    constructor() {
        this.type = ItemType.OpenQuestion;
        this.addButton = new AddButton(this);

        this.$container = null;
        this.$btn_delete = null;
        this.$btn_up = null;
        this.$btn_down = null;
        this.draw();
        this.setEvents();
    }

    draw() {
        let html = '';
        html += '<div class="card item-container">';
        html += '    <div class="card-header">';
        html += '        <div class="row justify-content-between">';
        html += '            <div class="col">';
        html += '                <input type="text" name="title" maxlength="150" required="" placeholder="Title" class="form-control">';
        html += '            </div>';
        html += '            <div class="col-auto form-inline">';
        html += '                <select class="form-control mr-2">';
        html += '                    <option>aa</option>';
        html += '                    <option>bb</option>';
        html += '                    <option>cc</option>';
        html += '                </select>';
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
        html += '</div>';
        this.$container = $(html);
        this.$btn_delete = this.$container.find('.item-cmd-delete');
        this.$btn_up = this.$container.find('.item-cmd-up');
        this.$btn_down = this.$container.find('.item-cmd-down');
    }

    setEvents()
    {
        this.$btn_delete.off('click').click(this.delete_click());
        this.$btn_up.off('click').click(this.up_click());
        this.$btn_down.off('click').click(this.down_click());
    }

    setButtonVisibility(index) {
        this.$btn_up.removeAttr('disabled');
        this.$btn_down.removeAttr('disabled');
        if(index === 0)
            this.$btn_up.attr('disabled', '');
        if(index === items.length-1)
            this.$btn_down.attr('disabled', '');
    }

    insertAtIndex(index, $prev) {
        if(!$prev)
        {
            if(index === 0)
                $prev = topAddButton.$container;
            else
                $prev = items[index-1].addButton.$container;
        }

        items.insert(index, this);
        this.$container.insertAfter($prev); //Insert items
        this.addButton.$container.insertAfter(this.$container); //Insert add button

        this.setEvents();
        this.addButton.setEvents();

        for(let i = 0; i < items.length; i++)
        {
            items[i].setButtonVisibility(i);
        }
    }

    remove() {
        this.$container.remove();
        this.addButton.remove();
        items.splice(items.indexOf(this), 1); //Remove item
    }

    delete_click() {
        let that = this
        return function ()
        {
            that.remove();
        };
    }

    up_click() {
        let that = this
        return function ()
        {
            let currentIndex = items.indexOf(that);
            let newIndex = Math.max((currentIndex-1), 0);

            that.remove();
            that.insertAtIndex(newIndex);
        };
    }

    down_click() {
        let that = this
        return function ()
        {
            let currentIndex = items.indexOf(that);
            let newIndex = Math.min((currentIndex+1), items.length-1);

            that.remove();
            that.insertAtIndex(newIndex);
        };
    }
}

class AddButton
{
    constructor(after) {
        this.after = after;
        this.$container = null;
        this.$button = null;
        this.draw();
        this.setEvents();
    }

    draw() {
        let html = '';
        html += '<div class="row mt-2 mb-2">';
        html +=     '<div class="col">';
        html +=         '<hr>';
        html +=     '</div>';
        html +=     '<div class="col-auto btn-group">';
        html +=         '<button class="btn btn-success" role="button" data-toggle="tooltip" data-placement="top" title="" data-original-title="Add new item">';
        html +=             '<i class="fas fa-plus"></i>';
        html +=         '</button>';
        html +=     '</div>';
        html +=     '<div class="col">';
        html +=         '<hr>';
        html +=     '</div>';
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
            if(that.after)
            {
                newIndex = items.indexOf(that.after) +1;
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
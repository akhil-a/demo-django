$(document).on("click", function(event){
        var $noti_icon = $('.notifications .icon_wrap');
        var $noti_dd = $('.notification_dd');
        var $profile_icon = $('.profile .icon_wrap');
        var $profile_dd = $('.profile_dd');
        if($noti_icon !== event.target && !$noti_icon.has(event.target).length && $noti_dd !== event.target && !$noti_dd.has(event.target).length){
            $(".notifications").removeClass("active");
        }
        if($profile_icon !== event.target && !$profile_icon.has(event.target).length && $profile_dd !== event.target && !$profile_dd.has(event.target).length){
            $(".profile").removeClass("active");
        }

    });


$(document).ready(function() {
    $('body').on('click', '.profile .icon_wrap', function(){
      $(this).parent().toggleClass("active");
      $(".notifications").removeClass("active");
    });
});


$(document).ready(function() {
    $('body').on('click', '.notifications .icon_wrap', function(){
      $(this).parent().toggleClass("active");
      $(".profile").removeClass("active");
    });
});


function step_process(from, to, dir) {
    if (typeof(dir) === 'undefined') dir = 'asc';
    var old_move = '';
    var new_start = '';

    var speed = 500;

    if (dir == 'asc') {
        old_move = '-';
        new_start = '';
    } else if (dir == 'desc') {
        old_move = '';
        new_start = '-';
    }

    $('#block'+from).animate({left: old_move+'100%'}, speed, function() {
        $(this).css({left: '100%', 'background-color':'transparent', 'z-index':'2'});
    });
    $('#block'+to).css({'z-index': '3', left:new_start+'100%'}).animate({left: '0%'}, speed, function() {
        $(this).css({'z-index':'2'});
    });

    if (Math.abs(from-to) === 1) {
        // Next Step
        if (from < to) $("#step"+from).addClass('complete').removeClass('current');
        else $("#step"+from).removeClass('complete').removeClass('current');
        var width = (parseInt(to) - 1) * 20;
        $(".progress_bar").find('.current_steps').animate({'width': width+'%'}, speed, function() {
            $("#step"+to).removeClass('complete').addClass('current');
        });
    } else {
        // Move to Step
        var steps = Math.abs(from-to);
        var step_speed = speed / steps;
        if (from < to) {
            move_to_step(from, to, 'asc', step_speed);
        } else {
            move_to_step(from, to, 'desc', step_speed);
        }
    }
}

function move_to_step(step, end, dir, step_speed) {
    if (dir == 'asc') {
        $("#step"+step).addClass('complete').removeClass('current');
        var width = (parseInt(step+1) - 1) * 20;
        $(".progress_bar").find('.current_steps').animate({'width': width+'%'}, step_speed, function() {
            $("#step"+(step+1)).removeClass('complete').addClass('current');
            if (step+1 < end) move_to_step((step+1), end, dir, step_speed);
        });
    } else {
        $("#step"+step).removeClass('complete').removeClass('current');
        var width = (parseInt(step-1) - 1) * 20;
        $(".progress_bar").find('.current_steps').animate({'width': width+'%'}, step_speed, function() {
            $("#step"+(step-1)).removeClass('complete').addClass('current');
            if (step-1 > end) move_to_step((step-1), end, dir, step_speed);
        });
    }
}

$(document).ready(function() {
    $("body").on("click", ".progress_bar .step.complete", function() {
        var from = $(this).parent().find('.current').data('step');
        var to = $(this).data('step');
        var dir = "desc";
        if (from < to) dir = "asc";

        step_process(from, to, dir);
    });
});


$(function() {
    $("#project_select_form").submit(function(event) {
        // Stop form from submitting normally
        event.preventDefault();
        $('.error-msg').css('display','none');
        var TestSuiteForm = $(this);
        // Send the data using post
        var posting = $.post( TestSuiteForm.attr('action'), TestSuiteForm.serialize() );
        // if success:
        posting.done(function(data) {
            console.log('posted')
            // success actions, maybe change submit button to 'friend added' or whatever
            console.log(data.project_status)
            console.log(data.devices)
//            step_process(2, 3);
            if(data.project_status == 1){
                $('#sel_device')
                    .find('option')
                    .remove()
                    .end()
                    .append('<option value="" selected disabled>Select Device ID</option>')
                    .val('')
                ;
                $('#sel_tc')
                    .empty()
                    .append('<ul><li><label for="select-all"><input type="checkbox" id="select-all" class="select-all-tc" value="Select All">Select All</label></li></ul>')
                    .find('.select-all-tc').click(function (){
                        $('input:checkbox').not(this).prop('checked', this.checked);
                    });

                for(i=0;i<data.devices.length;i++){
                    $(sel_device)
                        .append('<option value="' + data.devices[i] + '">' + data.devices[i] +'</option>')
                }
                for(i=0;i<data.tc_list.length;i++){
                    $("#sel_tc ul").append('<li><label for="tc_id_' + i +'"><input type="checkbox" name="tc_id" id="tc_id_' + i + '" value="' + data.tc_list[i] + '">' + data.tc_list[i] + '</label></li>');
                }
                step_process(2, 3);
            }
            else{
                console.log(data.project_error)
                $('#prj-error').css('display','block');
                $("#prj-error").empty();
                $('<i class=\"fa fa-times-circle\"></i><span>' + data.project_error + '</span>').appendTo('#prj-error');
            }
        });

        // if failure:
        posting.fail(function(data) {
            // 4xx or 5xx response, alert user about failure
            console.log(data); // log the returned json to the console
            var errors = jQuery.parseJSON(data)
            alert(errors)
        });
    });
});


$(function() {
    $("#device_select_form").submit(function(event) {
        // Stop form from submitting normally
        event.preventDefault();
        $('.error-msg').css('display','none');
        var TestSuiteForm = $(this);
        // Send the data using post
        var posting = $.post( TestSuiteForm.attr('action'), TestSuiteForm.serialize() );
        // if success:
        posting.done(function(data) {
            console.log('posted')
            // success actions, maybe change submit button to 'friend added' or whatever
            console.log(data.device_status)
            console.log(data.devices)
//            step_process(3, 4);
            if(data.device_status == 0){
                console.log(data.device_error)
                $('#device-error').css('display','block');
                $("#device-error").empty();
                $('<i class=\"fa fa-times-circle\"></i><span>' + data.device_error + '</span>').appendTo('#device-error');
            }
            else{
                step_process(3, 4);
            }
        });

        // if failure:
        posting.fail(function(data) {
            // 4xx or 5xx response, alert user about failure
            console.log(data); // log the returned json to the console
            var errors = jQuery.parseJSON(data)
            alert(errors)
        });
    });
});


$(function() {
    $("#tc_select_form").submit(function(event) {
        // Stop form from submitting normally
        event.preventDefault();
        $('.error-msg').css('display','none');
        var TestSuiteForm = $(this);
        // Send the data using post
        var posting = $.post( TestSuiteForm.attr('action'), TestSuiteForm.serialize() );
        // if success:
        posting.done(function(data) {
            console.log('posted')
            // success actions, maybe change submit button to 'friend added' or whatever
            console.log(data.tc_status)
            //step_process(4, 5);
            if(data.tc_status == 0){
                console.log(data.tc_error)
                $('#tc-error').css('display','block');
                $("#tc-error").empty();
                $('<i class=\"fa fa-times-circle\"></i><span>' + data.tc_error + '</span>').appendTo('#tc-error');
            }
            else{
                $('p#project-selection').text(data.project_selection)
                $('p#device-selection').text(data.device_selection)
                $('ul#tc-selection').empty()
                for(i=0;i<data.tc_selection.length;i++){
                    $('ul#tc-selection').append('<li><p class="selection-details">'+ data.tc_selection[i] +'</p></li>')
                }
                step_process(4, 5);
            }
        });

        // if failure:
        posting.fail(function(data) {
            // 4xx or 5xx response, alert user about failure
            console.log(data); // log the returned json to the console
            var errors = jQuery.parseJSON(data)
            alert(errors)
        });
    });
});


$(function() {
    $("#suite_valid_form").submit(function(event) {
        // Stop form from submitting normally
        event.preventDefault();
        var TestSuiteForm = $(this);
        // Send the data using post
        var posting = $.post( TestSuiteForm.attr('action'), TestSuiteForm.serialize() );
        // if success:
        posting.done(function(data) {
            console.log('Validation complete')
            if(data.test_suite_finish == 1){
                window.location.replace(data.tc_url);
            }
        });

        // if failure:
        posting.fail(function(data) {
            // 4xx or 5xx response, alert user about failure
            console.log(data); // log the returned json to the console
            var errors = jQuery.parseJSON(data)
            alert(errors)
        });
    });
});
// Main JavaScript for Twilio Bot Website

// Function to show loading spinner
function showLoading(button, message = 'অপেক্ষা করুন...') {
    const originalText = button.text();
    button.data('original-text', originalText)
        .prop('disabled', true)
        .html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${message}`);
    return originalText;
}

// Function to hide loading spinner
function hideLoading(button) {
    const originalText = button.data('original-text');
    button.prop('disabled', false).text(originalText);
}

// Function to show alert message
function showAlert(message, type = 'success') {
    const alertDiv = $(`<div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`);
    
    $('.container').first().prepend(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.alert('close');
    }, 5000);
}

// Document ready function
$(document).ready(function() {
    // Buy number form submission
    $('#buyNumberForm').submit(function(e) {
        e.preventDefault();
        
        const areaCode = $('#areaCode').val();
        const randomAreaCode = $('#areaCode').data('random') === true;
        const submitBtn = $(this).find('button[type="submit"]');
        
        showLoading(submitBtn);
        
        $.ajax({
            url: '/buy',
            method: 'POST',
            data: {
                area_code: areaCode,
                random_area_code: randomAreaCode
            },
            success: function(response) {
                if (response.success) {
                    showAlert(`নাম্বার সফলভাবে কেনা হয়েছে: ${response.phone_number}`, 'success');
                    location.reload(); // Reload to show the new number
                } else {
                    showAlert(`নাম্বার কিনতে সমস্যা: ${response.message}`, 'danger');
                }
            },
            error: function() {
                showAlert('সার্ভারে সমস্যা। আবার চেষ্টা করুন।', 'danger');
            },
            complete: function() {
                hideLoading(submitBtn);
                $('#areaCode').data('random', false);
            }
        });
    });
    
    // Random area code button
    $('#randomAreaCodeBtn').click(function() {
        $('#areaCode').val('').attr('placeholder', 'রেন্ডম কানাডিয়ান এরিয়া কোড').data('random', true);
        showAlert('রেন্ডম কানাডিয়ান এরিয়া কোড ব্যবহার করা হবে', 'info');
    });
    
    // Remove number form submission
    $('#removeNumberForm').submit(function(e) {
        e.preventDefault();
        
        const numberSid = $('#numberSelect').val();
        if (!numberSid) {
            showAlert('দয়া করে একটি নাম্বার নির্বাচন করুন', 'warning');
            return;
        }
        
        const submitBtn = $(this).find('button[type="submit"]');
        showLoading(submitBtn);
        
        $.ajax({
            url: '/remove',
            method: 'POST',
            data: {
                number_sid: numberSid
            },
            success: function(response) {
                if (response.success) {
                    showAlert('নাম্বার সফলভাবে রিমুভ করা হয়েছে', 'success');
                    location.reload(); // Reload to update the numbers list
                } else {
                    showAlert(`নাম্বার রিমুভ করতে সমস্যা: ${response.message}`, 'danger');
                }
            },
            error: function() {
                showAlert('সার্ভারে সমস্যা। আবার চেষ্টা করুন।', 'danger');
            },
            complete: function() {
                hideLoading(submitBtn);
                $('#removeNumberModal').modal('hide');
            }
        });
    });
    
    // Filter form submission for messages
    $('#filterForm').submit(function(e) {
        e.preventDefault();
        const phoneNumber = $('#phoneNumberFilter').val();
        window.location.href = '/messages' + (phoneNumber ? '?phone_number=' + encodeURIComponent(phoneNumber) : '');
    });
    
    // Refresh buttons
    $('.refresh-btn').click(function() {
        location.reload();
    });
    
    // View messages button
    $('.view-messages-btn').click(function() {
        const phoneNumber = $(this).data('number');
        window.location.href = '/messages?phone_number=' + encodeURIComponent(phoneNumber);
    });
    
    // Auto-refresh messages every 30 seconds on messages page
    if ($('#messagesList').length > 0) {
        setInterval(function() {
            const phoneNumber = $('#phoneNumberFilter').val();
            
            $.ajax({
                url: '/api/messages' + (phoneNumber ? '?phone_number=' + encodeURIComponent(phoneNumber) : ''),
                method: 'GET',
                success: function(response) {
                    if (response.success && response.messages.length > 0) {
                        // Check if there are new messages by comparing with current list
                        const currentCount = $('.message-item').length;
                        if (response.messages.length > currentCount) {
                            location.reload(); // Reload to show new messages
                        }
                    }
                }
            });
        }, 30000); // 30 seconds
    }
});

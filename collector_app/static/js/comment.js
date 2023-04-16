// ADD COMMENTS!!

$(document).ready(function() {
    // Show the add comment form when the button is clicked
    $('#add-comment-button').click(function(event) {
        event.preventDefault();
        console.log('button clicked');
        $('#add-comment-modal').modal('show');
    });

    // Submit the add comment form via AJAX
    $('#add-comment-form').submit(function(event) {
        event.preventDefault();
        console.log('submit button clicked');
        var form_data = $(this).serialize();
        console.log(form_data);
        var pk = $('#add-comment-button').data('profile-id');  // get the profile ID from the data attribute
        var url = '/profile/' + pk + '/comment/';
        
        console.log(url)
        $.ajax({
            url: url,
            type: 'POST',
            data: form_data,
            success: function(response) {
                // Hide the modal and reload the page
                console.log('we got this far');
                $('#add-comment-modal').modal('hide');
                window.location.href = '/profile/' + pk + '/';
            },
            error: function(response) {
                console.log(response);
            }
        });
    });
    
});

// DELETE COMMENTS!

$(document).ready(function() {
    // Delete comment
    $('.delete-comment-button').click(function(event) {
        event.preventDefault();
        var commentId = $(this).data('comment-id');
        var profileId = $(this).data('profile-id');
        console.log(commentId);
        if (confirm('Are you sure you want to delete this comment?')) {
            $.ajax({
                url: '/profile/' + profileId + '/comment/' + commentId + '/delete',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    $('#comment-' + commentId).remove();
                    location.reload();
                },
                error: function(response) {
                    alert('An error occurred while deleting the comment.');
                }
            });
        }
    });
});

// Edit comment
$(document).on('click', '.edit-comment-button', function(event) {
    event.preventDefault();
    var commentId = $(this).data('comment-id');
    var profileId = $(this).data('profile-id');
    var commentContent = $('#comment-' + commentId + '-content').text().trim();
    $('#edit-comment-content').val(commentContent);
    $('#edit-comment-form').attr('action', '/profile/' + profileId + '/comment/' + commentId + '/edit/');
    $('#edit-comment-modal').modal('show');
});

  // Handle form submission for editing comments
$('#edit-comment-form').submit(function(event) {
    event.preventDefault();
    var commentId = $(this).attr('action').split('/').slice(-2, -1)[0];
    var commentContent = $('#edit-comment-content').val();
    $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'content': commentContent
        },
        success: function(response) {
            $('#comment-' + commentId + '-content').text(commentContent);
            $('#edit-comment-modal').modal('hide');
            location.reload();
        },
        error: function(response) {
        alert('An error occurred while editing the comment.');
        }
    });
});


// SEARCH FUNCTION

$(document).ready(function() {
    $('#search-form').submit(function(event) {
        event.preventDefault(); // prevent default form submission
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                $('#users').html(data); // replace search results with updated results
            }
        });
    });
});

// VIEW USER 

$(document).ready(function() {
    $('#id_search_query').keyup(function() {
      var query = $(this).val();
      $.ajax({
        url: '/search/',
        type: 'GET',
        data: {
          'search_query': query
        },
        success: function(data) {
          $('#users').empty();
          if (data.results.length > 0) {
            $.each(data.results, function(i, user) {
              var profile_id = data.profiles[i].pk;
              var link = $('<a>').attr('href', '/profile/' + profile_id + '/').text(user.username);
              var paragraph = $('<p>').append(link);
              $('#users').append(paragraph);
            });
          } else {
            $('#users').append($('<p>').text('No matching users found.'));
          }
        }
      });
    });
  });
  

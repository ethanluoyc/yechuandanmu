var PostForm = React.createClass({
  handleSubmit: function(e) {
    e.preventDefault();
    var l = Ladda.create(document.querySelector('.ladda-button'));
    var form = this;
    this.setState({
      messages: []
    });
    l.toggle();
    $.post({
      url: 'post',
      cache: false,
      data: $('#sub').serialize(),
      dataType: 'json',
      success: function(data) {
        form.setState({messages: data.messages});
      }
    }).fail(function(jqxhr, textStatus, err) {
      if (jqxhr.status == 500) {
        const messages = [
          {body: '500: Internal Server Error', category: 'danger'}
        ];
        form.setState({messages: messages});
      } else if (jqxhr.status == 400) {
        form.setState({messages: jqxhr.responseJSON.messages});
      } else {
        const messages = [
          {body: 'Unknown error, maybe try a refresh?', category: 'danger'}
        ];
        form.setState({messages: jqxhr.responseJSON.messages});
      }
    }).always(function() {
      l.toggle();
  });
}, getInitialState : function() {
  return {
    messages: [],
    disabled: false
  };
}, render : function() {
  var msgs = this.state.messages.map(function(msg) {
    var cls = 'alert alert-' + msg.category;
    return (
      <div key={Date.now()} className={cls}>
        {msg.body}
      </div>
    );
  });
  return (
    <div>
      {msgs}
      <form id="sub" method="POST" action="" onSubmit={this.handleSubmit}>
        <input type="text" className="form-control" id="message" name="message" placeholder="弹幕内容"></input>
        <br/>
        <button id="my-button" type="submit" data-color="green" className="ladda-button" data-style="expand-right">
          <span className="ladda-label">Submit Danmaku</span>
        </button>
      </form>
    </div>
  );
}
});

$(document).ready(function() {
ReactDOM.render(
  <PostForm/>, document.getElementById('send'));
});

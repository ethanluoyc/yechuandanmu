var socket = io.connect('//' + document.domain + ':' + location.port + '/check')

var DanmuList = React.createClass({
  render: function() {
    var danmus = this.props.data.map(function(danmu) {
      return (
        <DanmuItem key={danmu.id} msg={danmu.data} status={danmu.status}/>
      )
    })
    return <table>
      <thead>
        <tr>
          <td>Content</td>
          <td>Status</td>
        </tr>
      </thead>
      <tbody>{danmus}</tbody>
    </table>
  }
})

var DanmuItem = React.createClass({
  render: function() {
    var status_arr = ['waiting', 'approved', 'disproved']
    return <tr>
      <td>{this.props.msg}</td>
      <td>{status_arr[this.props.status]}</td>
    </tr>
  }
})

var DanmuBox = React.createClass({
  componentDidMount: function() {
    socket.on('connect', function() {
      console.log('socket.io connected')
    })
    socket.on('check danmu', this.addDanmu) // Subscribe to stream from server

    var box = this
    window.addEventListener('keydown', function(e) {
      var msg = box.state.data[0]
      if (e.keyCode == 39) { // right arrow
        box.approveDanmu(msg)
      } else if (e.keyCode == 37) { // left arrow
        box.disproveDanmu(msg)
      }
    })
  },
  getInitialState: function() {
    var initialData = []
    return {data: initialData}
  },
  addDanmu: function(msg) {
    var newState = this.state.data.concat([msg])
    console.log(newState)
    this.setState({data: newState})
  },
  approveDanmu: function(msg) {
    console.log('approved', msg)
    socket.emit('approve danmu', msg)
    this.removeDanmu(msg)
  },
  disproveDanmu: function(msg) {
    console.log('disproved', msg)
    socket.emit('disprove danmu', msg)
    this.removeDanmu(msg)
  },
  flush: function() {
    this.state.data.map(function(msg) {
      this.approveDanmu(msg)
    })
  },
  removeDanmu: function(msg) {
    // console.log("Removed a danmu", msg)
    var index = this.state.data.indexOf(msg)
    if (index != -1) {
      var copyState = this.state.data.slice()
      copyState.splice(index, 1)
      this.setState({data: copyState})
    } else {console.log('the msg is not found!')}
  },
  render: function() {
    return (<div className="danmu">
      <h1>Danmu waiting for approval</h1>
      <DanmuList data={this.state.data}/>
    </div>)
  }
})

// setup the script
$(document).ready(function() {
  ReactDOM.render(
    <DanmuBox/>, document.getElementById('board'))
})

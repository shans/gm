class Model {
  constructor(json) {
    this.json = json;
    this.owner = undefined;
    // treat JSON information as a rules-free model
    if (!json.rules || !json.rules.initial) {
      for (var k in json)
        this[k] = json[k];
      if (!json.rules)
        return;
    }
    if (json.rules.initial) {
      for (var i of json.rules.initial) {
        this[i] = json.menus[i];
      }
    }
    this.result = {_shadow: {}}
    for (var i in json.rules) {
      if (i == 'initial')
        continue;
      // TODO: Don't need to define a property for objects that aren't rule
      // sources.
      (i => Object.defineProperty(this.result, i, {
        set: function(v) {
          this.unapplyRule(i, this.result._shadow[i]);
          this.result._shadow[i] = v;
          this.applyRule(i, v);
        }.bind(this),
        get: function() { return this.result._shadow[i]; }.bind(this)
      }))(i);
    }
  }

  setOwner(owner) {
    this.owner = owner;
  }

  unapplyRule(name, value) {
    if (value == "")
      return;
    var subnames = this.json.rules[name];
    if (typeof subnames == "string")
      subnames = [subnames];
    for (var subname of subnames) {
      this[subname] = undefined;
      this.owner.notifyPath('data.' + subname, undefined);
    }
  }

  applyRule(name, value) {
    if (value == "")
      return;
    var subnames = this.json.rules[name];
    if (typeof subnames == "string")
      subnames = [subnames];
    for (var subname of subnames) {
      var match = /(.*)\((.*)\)/.exec(subname);
      if (match) {
        subname = match[2];
        var content = this.json.menus[subname][value];
        var model = eval(match[1]);
        content = new model(content);
        // TODO: Track results
      } else {
        var content = this.json.menus[subname][value];
      }
      this[subname] = content;
      this.owner.notifyPath('data.' + subname, this[subname]);
    }
  }
}

% for version in data["versions"]:
% if version["tag"]:
open-notify-api (${version["tag"].strip('v')}) unstable; urgency=low


% for section in version["sections"]:
% for commit in section["commits"]:
  * ${commit["subject"]}
% endfor
% endfor
<%!from datetime import datetime%>
<%date = datetime.strptime(version["date"], "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S +0000")%>
 -- Nathan Bergey <nathan@open-notify.org>  ${date}

%endif
%endfor

import hashlib
import base64

old_script_content = """
        if (self === top) {
            var antiClickjack = document.getElementById("antiClickjack");
            if (antiClickjack) antiClickjack.parentNode.removeChild(antiClickjack);
        } else {
            top.location = self.location;
        }
    """
digest = hashlib.sha256(old_script_content.encode('utf-8')).digest()
print("old sha256-" + base64.b64encode(digest).decode('utf-8'))

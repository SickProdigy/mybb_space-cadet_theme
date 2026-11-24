<?php
/** Render generated/imported MyBB templates with synthetic saved/preview post contexts. */
error_reporting(E_ALL);
set_error_handler(function($severity,$message,$file,$line){throw new RuntimeException($message.' at '.$line);});
$source=getenv('SPACE_CADET_IMPORTED_TEMPLATES');
if($source){$templates=json_decode(file_get_contents($source),true,512,JSON_THROW_ON_ERROR);}
else{
    $xml=simplexml_load_file(__DIR__.'/../space-cadet-theme.xml');$templates=array();
    foreach($xml->templates->template as $t){$templates[(string)$t['name']]=(string)$t;}
}
function renderPost($name,$saved,$pid,$permalink,$staff){
    global $templates;
    $body=$templates[$name];$post=array();
    preg_match_all('/\{\$post\[\'([^\']+)\'\]\}/',$body,$fields);
    foreach($fields[1] as $field){$post[$field]='';}
    $post['pid']=$pid;$post['message']='Synthetic post';$post['subject_title']='Fixture';
    $post['posturl']=$saved?'<div class="post_number"><a href="'.htmlspecialchars($permalink,ENT_QUOTES,'UTF-8').'">#1</a></div>':'';
    if($staff){$post['button_warn']='<a class="postbit_warn" href="#warn">Warn</a>';$post['button_purgespammer']='<a class="postbit_purgespammer" href="#purge">Purge Spammer</a>';}
    // Preview, PM and announcement contexts intentionally have no postlink key.
    unset($post['postlink']);
    $ignore_bit=$deleted_bit=$unapproved_shade=$post_visibility='';
    eval('$html = "'.str_replace("\\'","'",addslashes($body)).'";');
    return $html;
}
$origin='http://'.($_SERVER['HTTP_HOST'] ?? 'web:8000');
$cases=array('normal'=>array('postbit',true,42,$origin.'/showthread.php?tid=5&pid=42#pid42',true),
    'classic'=>array('postbit_classic',true,43,$origin.'/thread-5-post-43.html#pid43',true),
    'reply-preview'=>array('postbit',false,0,'',false),'newthread-preview'=>array('postbit_classic',false,0,'',false),
    'pm'=>array('postbit',false,123,'',false),'announcement'=>array('postbit_classic',false,456,'',false),
    'external'=>array('postbit',true,44,'https://foreign.example/post#pid44',false),
    'no-post-anchor'=>array('postbit_classic',true,45,$origin.'/showthread.php?tid=5',false),
    'member'=>array('postbit',true,46,$origin.'/showthread.php?tid=5&pid=46#pid46',false));
$posts='';foreach($cases as $name=>$args){$posts.='<section data-case="'.$name.'">'.renderPost(...$args).'</section>';}
$show=$templates['showthread'];$start=strpos($show,'(function() {');$end=strpos($show,'})();',$start)+5;$script=substr($show,$start,$end-$start);
$script=str_replace('{$thread[\'firstpost\']}','42',$script);
$css=$templates['__css']??'';
if($css===''){$stylesheet=simplexml_load_file(__DIR__.'/../theme_overrides/stylesheets/space_cadet.css.xml');$css=(string)$stylesheet;}
$extra=str_replace('</script>','<\/script>',json_encode(renderPost('postbit',true,99,$origin.'/showthread.php?tid=5&pid=99#pid99',false),JSON_HEX_TAG|JSON_HEX_AMP));
?><!doctype html><html><head><meta charset="utf-8"><title>Space Cadet fixture</title><style><?php echo $css; ?></style></head><body>
<form id="moderator_options"><select id="moderator_options_selector"><option value="">Choose</option><option value="openclosethread">Open / Close</option></select></form>
<div class="showthread_share_tool"><div class="portal_share"><button class="showthread_share_toggle" data-board-url="<?=htmlspecialchars($origin,ENT_QUOTES,'UTF-8')?>" data-thread-id="5">Share thread</button><div class="portal_share_menu" hidden><input class="showthread_share_url"><button class="showthread_native_share"></button><a class="showthread_email_share"></a><a class="showthread_facebook_share"></a><a class="showthread_x_share"></a><a class="showthread_reddit_share"></a><button class="showthread_copy_share"></button></div></div></div>
<div id="posts"><?php echo $posts; ?></div>
<script><?php echo $script; ?></script>
<script>
(function() {
    var passed = [];
    function check(ok, message) { if (!ok) throw new Error(message); passed.push(message); }
    window.addEventListener('error', function(event) { document.body.dataset.tests = 'failed: ' + event.message; });
    function item(name) { return document.querySelector('[data-case="' + name + '"] .postbit_share_wrap'); }
    try {
        ['normal','classic','member'].forEach(function(name) {
            var share = item(name);
            check(!share.hidden, name + ' share visible');
            share.querySelector('.showthread_share_toggle').click();
            check(!share.querySelector('.portal_share_menu').hidden, name + ' dialog opens');
            check(/#pid[1-9][0-9]*$/.test(share.querySelector('.showthread_share_url').value), name + ' saved permalink');
            document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape'}));
            check(share.querySelector('.portal_share_menu').hidden, name + ' Escape closes');
        });
        ['reply-preview','newthread-preview','pm','announcement','external','no-post-anchor'].forEach(function(name) {
            check(item(name).hidden && getComputedStyle(item(name)).display === 'none', name + ' share hidden');
            check(item(name).querySelector('.portal_share_menu').hidden, name + ' panel hidden');
        });
        var opening = document.getElementById('post_42');
        check(!!opening.querySelector('.postbit_warn'), 'opening Warn retained');
        check(!!opening.querySelector('.postbit_purgespammer'), 'opening Purge retained');
        check(!!opening.querySelector('.postbit_thread_action'), 'thread moderation retained');
        check(document.querySelector('[data-case="member"] .postbit_moderate_wrap').hidden, 'member moderation absent');
        var extra = document.createElement('section'); extra.dataset.case = 'dynamic'; extra.innerHTML = <?php echo $extra; ?>;
        document.getElementById('posts').appendChild(extra);
        setTimeout(function() {
            try {
                var share = item('dynamic'); check(!share.hidden, 'new reply share initialized');
                share.querySelector('.showthread_share_toggle').click();
                check(!share.querySelector('.portal_share_menu').hidden, 'new reply dialog opens once');
                document.body.dataset.tests = 'passed'; document.body.dataset.checks = String(passed.length);
            } catch (error) { document.body.dataset.tests = 'failed: ' + error.message; }
        }, 50);
    } catch (error) { document.body.dataset.tests = 'failed: ' + error.message; }
}());
</script></body></html>

# 贡献指南

欢迎提交 issue 与 PR。这个项目的核心价值在**方法论的正确性**，所以请优先关注以下几条。

## 提交前必须做

```bash
python -m py_compile tools/*.py        # 语法
python tools/preflight.py --root . --strict   # 合规自检（必须为绿）
```

CI 也会跑这两条，红了不会合并。

## 不要提交

- 任何**真实人物**的聊天记录、AI 会话、日记、照片
- `corpus/`、`lives/`、`exports/`、`work/`、`versions/`、`third_party/`
- `*.wechat_exp_config.json`（含微信数据库解密密钥）
- 凭据、手机号、邮箱、真实 wxid、身份证、银行卡号

需要在文档里示范敏感词时，在那一行加上 `<!-- preflight:ignore -->`（行内豁免）。

## 修改人格方法论时的注意事项

1. **不要把单场景行为写成稳定特征**（见 `docs/LESSONS.md`）
2. **加分项要带使用条件**，不要只写"高频"——频率不等于用法
3. 改动若影响生成物行为，请同步更新 `prompts/analyzer.md`、`templates/persona.template.md` 与 `docs/METHOD.md`
4. 新增第三方依赖要同步更新 `THIRD_PARTY_NOTICES.md`

## 提交信息

用中文或英文都可以，建议格式：

```
feat: 支持 QQ mht 导出解析
fix: 修复 txt 解析丢掉跨行正文的问题
docs: 补充 WeFlow 署名说明
```

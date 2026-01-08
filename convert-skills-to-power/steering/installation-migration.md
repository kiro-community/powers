# Installation and Migration Guide

## Installation Mechanism Comparison

### Claude Skills Installation

**Process:**
```
1. Create directory: mkdir ~/.claude/skills/my-skill
2. Create SKILL.md file
3. Add supporting files (optional)
4. Restart Claude Code
5. Wait for Skills to load
```

**Time:** 5-10 minutes (including restart)

**Characteristics:**
- ❌ Manual file creation
- ❌ Requires restart
- ❌ No version management
- ❌ No dependency checking
- ❌ No official market

### Kiro Powers Installation

**Process:**
```
1. Open Powers panel in Kiro
2. Search or browse Powers
3. Click "Install"
4. Configure if needed (API keys, etc.)
5. Use immediately
```

**Time:** 30 seconds - 1 minute

**Characteristics:**
- ✅ One-click installation
- ✅ Immediate effect (no restart)
- ✅ Automatic version management
- ✅ Dependency detection
- ✅ Official marketplace

## Installation Methods Comparison

| Method | Claude Skills | Kiro Powers |
|--------|--------------|-------------|
| **Official Market** | ❌ None | ✅ kiro.dev |
| **GitHub** | Manual clone | ✅ URL import |
| **Local** | Copy files | ✅ Directory import |
| **Enterprise** | Admin config | ✅ Enterprise market |
| **CLI** | ❌ None | ✅ `kiro power install` |

## Migration Strategies

### Strategy 1: Gradual Migration (Recommended)

**Best for:** Teams with many Skills, production environments

**Approach:**
```
Week 1-2: Convert 2-3 simple Skills
  ├─ Test thoroughly
  ├─ Gather feedback
  └─ Refine process

Week 3-4: Convert script-based Skills
  ├─ Use Script Executor Pattern
  ├─ Test MCP integration
  └─ Document issues

Week 5-6: Convert remaining Skills
  ├─ Batch conversion
  ├─ Team training
  └─ Full deployment

Week 7+: Maintenance and optimization
  ├─ Monitor performance
  ├─ Collect feedback
  └─ Iterate improvements
```

**Benefits:**
- Lower risk
- Time to learn
- Feedback incorporation
- Team adaptation

### Strategy 2: Big Bang Migration

**Best for:** Small teams, few Skills, non-critical environments

**Approach:**
```
Day 1: Convert all Skills
  ├─ Use automated tools
  ├─ Batch conversion
  └─ Quick testing

Day 2: Deploy and test
  ├─ Install all Powers
  ├─ Functional testing
  └─ Fix critical issues

Day 3+: Refinement
  ├─ Address feedback
  ├─ Optimize performance
  └─ Update documentation
```

**Benefits:**
- Fast completion
- Clean cutover
- Immediate benefits

**Risks:**
- Higher initial disruption
- More issues at once
- Less learning time

### Strategy 3: Hybrid Approach

**Best for:** Medium teams, mixed Skill complexity

**Approach:**
```
Phase 1: Critical Skills (Week 1-2)
  └─ Convert most-used Skills first

Phase 2: Script-based Skills (Week 3-4)
  └─ Focus on MCP conversion using Script Executor Pattern

Phase 3: Remaining Skills (Week 5-6)
  └─ Batch convert simple Skills

Phase 4: Optimization (Week 7+)
  └─ Refine and improve
```

## Team Migration Checklist

### Pre-Migration (1-2 weeks before)

- [ ] Audit all existing Skills
- [ ] Identify dependencies
- [ ] Prioritize conversion order
- [ ] Set up conversion environment
- [ ] Train conversion team
- [ ] Create backup of Skills
- [ ] Communicate plan to team

### During Migration

- [ ] Convert Skills to Powers
- [ ] Test each Power thoroughly
- [ ] Document conversion decisions
- [ ] Track issues and solutions
- [ ] Update team documentation
- [ ] Provide training sessions
- [ ] Gather feedback continuously

### Post-Migration

- [ ] Monitor Power usage
- [ ] Collect performance metrics
- [ ] Address feedback
- [ ] Optimize as needed
- [ ] Update documentation
- [ ] Share lessons learned
- [ ] Plan future improvements

## Installation Workflows

### Workflow 1: Individual Developer

**Installing a Power:**
```
1. Open Kiro IDE
2. Click Kiro icon → Powers
3. Search for Power
4. Click "Install"
5. Configure if prompted
6. Start using immediately
```

**Installing from GitHub:**
```
1. Open Powers panel
2. Click "Import from GitHub"
3. Enter URL: https://github.com/user/power
4. Click "Import"
5. Power installs automatically
```

**Installing from Local:**
```
1. Open Powers panel
2. Click "Import from Folder"
3. Select Power directory
4. Click "Import"
5. Power installs immediately
```

### Workflow 2: Team Distribution

**Option A: GitHub Repository**
```bash
# 1. Create team Powers repository
git init team-powers
cd team-powers

# 2. Add converted Powers
cp -r ../converted-powers/* ./

# 3. Push to GitHub
git add .
git commit -m "Add team Powers"
git remote add origin https://github.com/team/powers
git push -u origin main

# 4. Share with team
# Team members install via GitHub URL
```

**Option B: Internal Package Registry**
```bash
# 1. Package Powers
tar -czf team-powers.tar.gz converted-powers/

# 2. Upload to internal registry
# (Company-specific process)

# 3. Team installs from registry
kiro power install internal://team-powers
```

### Workflow 3: Enterprise Deployment

**Setup Enterprise Market:**
```
1. Access enterprise control panel
2. Create private market
3. Upload Powers
4. Configure permissions:
   - Mandatory Powers (auto-install)
   - Recommended Powers (suggested)
   - Restricted Powers (blocked)
5. Set update policies
6. Enable usage tracking
```

**User Experience:**
```
1. User opens Kiro
2. Mandatory Powers auto-install
3. Recommended Powers show notification
4. User can browse enterprise market
5. Updates apply automatically
```

## Version Management

### Claude Skills (Manual)

```bash
# No built-in versioning
# Manual approach:

# 1. Tag in Git
git tag v1.0.0
git push --tags

# 2. Users manually update
cd ~/.claude/skills/my-skill
git pull
# Restart Claude Code
```

### Kiro Powers (Automatic)

```bash
# Check for updates
kiro power list
# Shows: my-power v1.0.0 → v1.2.0 available

# Update single Power
kiro power update my-power

# Update all Powers
kiro power update --all

# Rollback if needed
kiro power install my-power@1.0.0
```

## Dependency Management

### Claude Skills

**Manual approach:**
```markdown
# In SKILL.md
## Dependencies
- Python 3.8+
- PyPDF2: `pip install PyPDF2`
- Pillow: `pip install Pillow`

## Installation
```bash
pip install -r requirements.txt
```
```

**User must:**
- Read documentation
- Install dependencies manually
- Verify versions
- Troubleshoot conflicts

### Kiro Powers

**Automatic approach:**
```yaml
# In POWER.md frontmatter
dependencies:
  system:
    - python: ">=3.8"
  python:
    - PyPDF2: "^2.0.0"
    - Pillow: "~8.3.0"
  powers:
    - name: file-utils
      version: "^1.0.0"
```

**System handles:**
- Dependency detection
- Automatic installation
- Version validation
- Conflict resolution

## Performance Comparison

### Context Usage

**Claude Skills:**
```
All Skills loaded at startup
├─ Skill 1: 2KB
├─ Skill 2: 5KB
├─ Skill 3: 3KB
├─ Skill 4: 8KB
└─ Skill 5: 4KB
Total: 22KB always in context
```

**Kiro Powers:**
```
Powers loaded on-demand
├─ Power 1: Activated → 2KB
├─ Power 2: Not used → 0KB
├─ Power 3: Activated → 3KB
├─ Power 4: Not used → 0KB
└─ Power 5: Activated → 4KB
Total: 9KB (59% reduction)
```

### Startup Time

| Metric | Claude Skills | Kiro Powers |
|--------|--------------|-------------|
| **Initial Load** | All Skills | None |
| **Activation** | N/A | On keyword |
| **Deactivation** | N/A | Automatic |
| **Restart Required** | Yes | No |

## Migration Timeline Example

### Small Team (5 Skills)

```
Week 1:
  Mon-Tue: Convert 2 simple Skills
  Wed-Thu: Convert 2 script Skills
  Fri: Convert 1 complex Skill
  
Week 2:
  Mon-Tue: Test all Powers
  Wed: Deploy to team
  Thu-Fri: Support and fixes

Total: 2 weeks
```

### Medium Team (15 Skills)

```
Week 1-2: Convert simple Skills (5)
Week 3-4: Convert script Skills (7)
Week 5-6: Convert complex Skills (3)
Week 7: Testing and refinement
Week 8: Deployment and training

Total: 8 weeks
```

### Large Team (50+ Skills)

```
Month 1: Pilot (10 Skills)
  ├─ Convert and test
  ├─ Gather feedback
  └─ Refine process

Month 2-3: Main conversion (30 Skills)
  ├─ Batch conversion
  ├─ Parallel testing
  └─ Gradual deployment

Month 4: Remaining Skills (10+ Skills)
  ├─ Complex conversions
  ├─ Edge cases
  └─ Final deployment

Month 5+: Optimization
  ├─ Performance tuning
  ├─ User feedback
  └─ Continuous improvement

Total: 5+ months
```

## Cost-Benefit Analysis

### Conversion Costs

| Activity | Time per Skill | Cost Factor |
|----------|---------------|-------------|
| Simple conversion | 1-2 hours | Low |
| Script conversion | 2-4 hours | Medium |
| Complex conversion | 1-2 days | High |
| Testing | 30 min - 1 hour | Low |
| Documentation | 1-2 hours | Low |

### Benefits

| Benefit | Impact | Timeline |
|---------|--------|----------|
| Reduced context usage | 30-50% | Immediate |
| Faster installation | 10x faster | Immediate |
| Version management | High | Immediate |
| Team productivity | 20-40% | 1-3 months |
| Maintenance reduction | 50% | 3-6 months |

### ROI Calculation

```
Example: 10 Skills, 5-person team

Conversion Cost:
- 10 Skills × 3 hours avg = 30 hours
- 30 hours × $100/hour = $3,000

Monthly Benefit:
- Context savings: 8 hours/month
- Installation time: 2 hours/month
- Maintenance: 5 hours/month
- Total: 15 hours/month × $100/hour = $1,500/month

ROI: 2 months to break even
Year 1 savings: $15,000
```

## Best Practices

### Communication

1. **Announce Early**
   - Share migration plan
   - Explain benefits
   - Address concerns

2. **Provide Training**
   - Powers overview
   - Installation guide
   - Troubleshooting tips

3. **Gather Feedback**
   - Regular check-ins
   - Issue tracking
   - Continuous improvement

### Technical

1. **Test Thoroughly**
   - Functional testing
   - Performance testing
   - Integration testing

2. **Document Everything**
   - Conversion decisions
   - Issues encountered
   - Solutions applied

3. **Monitor Performance**
   - Context usage
   - Activation patterns
   - Error rates

### Organizational

1. **Phased Rollout**
   - Start with volunteers
   - Expand gradually
   - Full deployment last

2. **Support Plan**
   - Dedicated support channel
   - FAQ document
   - Quick response team

3. **Success Metrics**
   - Adoption rate
   - User satisfaction
   - Performance improvements

---

**Next Steps:**
- Choose migration strategy
- Create detailed timeline
- Communicate with team
- Begin conversion process
